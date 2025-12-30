from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InputFile, FSInputFile
from aiogram.fsm.context import FSMContext
import random
from asgiref.sync import sync_to_async

from apps.models import BotUser, Question, TestAttempt, AttemptDetail
from apps.bot.keyboards import main_menu, test_options
from apps.bot.states import Registration, TestState

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await sync_to_async(BotUser.objects.filter(telegram_id=user_id).first)()
    
    if not user:
        await message.answer("Assalawma aleykum! Testti baslaw ushın atı-familiyańızdı kiritin:")
        await state.set_state(Registration.waiting_for_full_name)
    else:
        await message.answer(f"Xosh keldıńiz, {user.full_name}!", reply_markup=main_menu())

@router.message(Registration.waiting_for_full_name)
async def process_name(message: Message, state: FSMContext):
    full_name = message.text
    user_id = message.from_user.id
    username = message.from_user.username
    
    await sync_to_async(BotUser.objects.create)(
        telegram_id=user_id,
        full_name=full_name,
        username=username
    )
    
    await message.answer(f"Raxmet, {full_name}! Registraciya pitkırıldı.", reply_markup=main_menu())
    await state.clear()

@router.message(F.text == "📊 Meniń nátiyjelerim")
async def show_results(message: Message):
    user_id = message.from_user.id
    user = await sync_to_async(BotUser.objects.filter(telegram_id=user_id).first)()
    
    if not user:
        await message.answer("Siz dizimnen ótpepsiz. /start komandasın jiberiń.")
        return
        
    attempts = await sync_to_async(list)(
        TestAttempt.objects.filter(user=user).order_by('-created_at')[:10]
    )
    
    if not attempts:
        await message.answer("Sizde ele nátiyjeler joq.")
        return
        
    text = "Sizdıń sońǵı 10 nátiyjeńiz:\n\n"
    for i, a in enumerate(attempts, 1):
        text += f"{i}. {a.created_at.strftime('%d.%m.%Y %H:%M')} - {a.score}/{a.total_questions}\n"
        
    await message.answer(text)

@router.message(F.text == "🎯 Test baslaw")
async def start_test(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await sync_to_async(BotUser.objects.filter(telegram_id=user_id).first)()
    
    if not user:
        await message.answer("Siz dizimnen ótpepsiz. /start komandasın jiberiń.")
        return

    # Get 10 random active questions
    all_questions = await sync_to_async(list)(Question.objects.filter(is_active=True))
    if len(all_questions) < 1:
        await message.answer("Bazada sorawlar joq. Adminge xabar beriń.")
        return
        
    selected_questions = random.sample(all_questions, min(len(all_questions), 10))
    question_ids = [q.id for q in selected_questions]
    
    # Store test data in FSM
    await state.update_data(
        question_ids=question_ids,
        current_index=0,
        answers={} # Dict: {question_id: user_answer_char}
    )
    
    await state.set_state(TestState.taking_test)
    await send_next_question(message, state)

async def send_next_question(message, state: FSMContext):
    data = await state.get_data()
    idx = data['current_index']
    q_ids = data['question_ids']
    answers = data.get('answers', {})
    
    # Finish if beyond last question (happens on Next from last)
    # But wait, user might want to go back? 
    # Logic: If index == len, we finish.
    if idx >= len(q_ids):
        await finish_test(message, state)
        return
        
    q_id = q_ids[idx]
    question = await sync_to_async(Question.objects.get)(id=q_id)
    
    # Check if previously answered
    prev_ans = answers.get(str(q_id)) # FSM serializes keys to strings sometimes
    prev_ans_text = f" (Sizdiń juwabıńız: {prev_ans.upper()})" if prev_ans else ""
    
    text = f"Soraw {idx + 1}/{len(q_ids)}{prev_ans_text}:\n\n{question.text}\n\n"
    text += f"A) {question.option_a}\n"
    text += f"B) {question.option_b}\n"
    text += f"C) {question.option_c}\n"
    text += f"D) {question.option_d}\n"
    
    if question.image:
        photo = FSInputFile(question.image.path)
        await message.answer_photo(photo, caption=text, reply_markup=test_options())
    else:
        await message.answer(text, reply_markup=test_options())

@router.callback_query(TestState.taking_test, F.data.startswith("ans_"))
async def handle_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    idx = data['current_index']
    q_ids = data['question_ids']
    answers = data.get('answers', {})
    q_id = q_ids[idx]
    
    action = callback.data.split("_")[1] # a, b, c, d, back, next
    
    # Handle logic
    if action == "back":
        if idx > 0:
            new_idx = idx - 1
        else:
            await callback.answer("Basiında turıpsız!") # At the beginning
            return
    elif action == "next":
        # Skip logic - user chose nothing for this question
        new_idx = idx + 1
    else:
        # User answered a/b/c/d
        answers[str(q_id)] = action
        new_idx = idx + 1
    
    # Update State
    await state.update_data(current_index=new_idx, answers=answers)
    
    # UI Cleanup
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass # Message might be too old or other error
        
    await send_next_question(callback.message, state)
    await callback.answer()

async def finish_test(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.chat.id
    user = await sync_to_async(BotUser.objects.get)(telegram_id=user_id)
    
    answers = data.get('answers', {})
    q_ids = data['question_ids']
    
    score = 0
    # Calculate score
    for q_id in q_ids:
        q = await sync_to_async(Question.objects.get)(id=q_id)
        user_ans = answers.get(str(q_id))
        if user_ans and user_ans == q.correct_answer:
            score += 1
            
    # Save Attempt
    attempt = await sync_to_async(TestAttempt.objects.create)(
        user=user,
        score=score,
        total_questions=len(q_ids)
    )
    
    # Save Details
    detail_errors = []
    
    for q_id in q_ids:
        q = await sync_to_async(Question.objects.get)(id=q_id)
        user_ans = answers.get(str(q_id))
        is_correct = (user_ans == q.correct_answer)
        
        await sync_to_async(AttemptDetail.objects.create)(
            attempt=attempt,
            question=q,
            user_answer=user_ans,
            is_correct=is_correct
        )
        
        if not is_correct:
            detail_errors.append((q, user_ans))
            
    result_text = f"Test juwmaqlandı!\n\nSizdıń nátiyjeńiz: {score}/{len(q_ids)}\n\n"
    
    if detail_errors:
        result_text += "Qáte qılǵan sorawlarıńız:\n"
        for i, (q, user_ans) in enumerate(detail_errors, 1):
            user_ans_label = user_ans.upper() if user_ans else "Belgilenbegen" # Skipped/Empty
            result_text += f"{i}. {q.text[:30]}... (Siz: {user_ans_label} ❌, Durıs: {q.correct_answer.upper()} ✅)\n"
            
    await message.answer(result_text, reply_markup=main_menu())
    await state.clear()

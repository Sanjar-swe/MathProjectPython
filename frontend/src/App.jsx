import React, { useState, useEffect } from 'react';
import { LayoutDashboard, FileSpreadsheet, Users, Shield, Upload, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [uploadStatus, setUploadStatus] = useState(null); // success, error, uploading
  
  // Data states
  const [stats, setStats] = useState({ total_users: 0, total_attempts: 0, top_users: [] });
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch Dashboard Stats
  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/attempts/dashboard/');
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (e) {
      console.error("Failed to fetch stats", e);
    }
  };

  // Fetch Students List
  const fetchStudents = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/users/');
      if (response.ok) {
        const data = await response.json();
        setStudents(data);
      }
    } catch (e) {
      console.error("Failed to fetch students", e);
    } finally {
      setLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    fetchStats();
  }, []);

  // Fetch students when tab changes
  useEffect(() => {
    if (activeTab === 'students') {
      fetchStudents();
    }
    if (activeTab === 'dashboard') {
      fetchStats();
    }
  }, [activeTab]);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    
    setUploadStatus('uploading');
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await fetch('http://localhost:8000/api/questions/import-excel/', {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        setUploadStatus('success');
      } else {
        setUploadStatus('error');
      }
    } catch (e) {
      setUploadStatus('error');
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 text-gray-900 font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-xl z-10 flex flex-col">
        <div className="p-6 border-b border-gray-100 flex items-center gap-2">
           <Shield className="w-8 h-8 text-blue-600" />
           <span className="text-xl font-bold text-gray-800">UStudy Admin</span>
        </div>
        
        <nav className="flex-1 p-4 space-y-2">
          <SidebarItem icon={<LayoutDashboard />} label="Дашборд" active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
          <SidebarItem icon={<FileSpreadsheet />} label="Вопросы" active={activeTab === 'questions'} onClick={() => setActiveTab('questions')} />
          <SidebarItem icon={<Users />} label="Ученики" active={activeTab === 'students'} onClick={() => setActiveTab('students')} />
        </nav>
        
        <div className="p-4 border-t border-gray-100">
           <div className="text-xs text-gray-400">Версия 1.0.1</div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto p-8">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
                {activeTab === 'dashboard' && 'Обзор статистики'}
                {activeTab === 'questions' && 'Управление вопросами'}
                {activeTab === 'students' && 'Список учеников'}
            </h1>
            <p className="text-gray-500 mt-2">Добро пожаловать в панель управления учителя.</p>
          </div>
          <button onClick={() => activeTab === 'students' ? fetchStudents() : fetchStats()} className="p-2 bg-white rounded-full shadow-sm hover:shadow-md transition-all text-gray-500 hover:text-blue-600">
            <RefreshCw size={20} />
          </button>
        </header>

        {activeTab === 'dashboard' && (
            <div className="space-y-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <StatCard title="Всего учеников" value={stats.total_users} />
                    <StatCard title="Всего попыток" value={stats.total_attempts} />
                    {/* Simplified average for now, ideally calc on backend */}
                    <StatCard title="Топ результат" value={stats.top_users.length > 0 ? `${stats.top_users[0].score}/10` : '-'} />
                </div>
                
                <div>
                     <h2 className="text-xl font-semibold mb-4">Топ-10 Учеников</h2>
                     <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                        <table className="w-full text-left">
                            <thead className="bg-gray-50 border-b border-gray-100">
                                <tr>
                                    <th className="p-4 font-semibold text-gray-600">Имя</th>
                                    <th className="p-4 font-semibold text-gray-600">Результат</th>
                                    <th className="p-4 font-semibold text-gray-600">Дата</th>
                                </tr>
                            </thead>
                            <tbody>
                                {stats.top_users.map((attempt) => (
                                    <tr key={attempt.id} className="border-b border-gray-50 hover:bg-gray-50">
                                        <td className="p-4 font-medium">{attempt.user_name}</td>
                                        <td className="p-4">
                                            <span className="bg-green-100 text-green-700 px-2 py-1 rounded-lg text-sm font-bold">
                                                {attempt.score}/{attempt.total_questions}
                                            </span>
                                        </td>
                                        <td className="p-4 text-gray-500 text-sm">
                                            {new Date(attempt.created_at).toLocaleDateString()}
                                        </td>
                                    </tr>
                                ))}
                                {stats.top_users.length === 0 && (
                                    <tr><td colSpan="3" className="p-8 text-center text-gray-400">Нет данных</td></tr>
                                )}
                            </tbody>
                        </table>
                     </div>
                </div>
            </div>
        )}

        {activeTab === 'questions' && (
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 max-w-2xl mx-auto text-center">
            <div className="mb-6 flex justify-center">
              <div className="bg-blue-50 p-4 rounded-full">
                <Upload className="w-12 h-12 text-blue-600" />
              </div>
            </div>
            <h2 className="text-xl font-semibold mb-2">Загрузить вопросы из Excel</h2>
            <p className="text-gray-500 mb-8">Перетащите файл сюда или нажмите кнопку для выбора.</p>
            
            <label className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-medium cursor-pointer transition-all active:scale-95">
              <span>Выбрать файл (.xlsx)</span>
              <input type="file" className="hidden" accept=".xlsx" onChange={handleFileUpload} />
            </label>

            {uploadStatus === 'uploading' && <p className="mt-4 text-blue-600 animate-pulse">Загрузка...</p>}
            {uploadStatus === 'success' && (
              <div className="mt-4 flex items-center justify-center gap-2 text-green-600">
                <CheckCircle className="w-5 h-5" />
                <span>Вопросы успешно добавлены!</span>
              </div>
            )}
            {uploadStatus === 'error' && (
              <div className="mt-4 flex items-center justify-center gap-2 text-red-600">
                <AlertCircle className="w-5 h-5" />
                <span>Ошибка загрузки. Проверьте формат файла.</span>
              </div>
            )}
          </div>
        )}
        
        {activeTab === 'students' && (
             <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                <div className="p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
                    <h3 className="font-semibold text-gray-700">Все зарегистрированные ученики</h3>
                    <span className="text-sm text-gray-500">Всего: {students.length}</span>
                </div>
                <table className="w-full text-left">
                    <thead>
                        <tr className="border-b border-gray-100 text-sm uppercasetracking-wider text-gray-500">
                            <th className="p-4 font-semibold">ID (Telegram)</th>
                            <th className="p-4 font-semibold">ФИО</th>
                            <th className="p-4 font-semibold">Username</th>
                            <th className="p-4 font-semibold">Дата регистрации</th>
                        </tr>
                    </thead>
                    <tbody>
                        {students.map((student) => (
                            <tr key={student.id} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                                <td className="p-4 font-mono text-sm text-blue-600">{student.telegram_id}</td>
                                <td className="p-4 font-medium text-gray-900">{student.full_name}</td>
                                <td className="p-4 text-gray-500">{student.username ? `@${student.username}` : '-'}</td>
                                <td className="p-4 text-gray-400 text-sm">
                                    {new Date(student.created_at).toLocaleDateString()}
                                </td>
                            </tr>
                        ))}
                         {students.length === 0 && !loading && (
                            <tr><td colSpan="4" className="p-8 text-center text-gray-400">Список пуст</td></tr>
                        )}
                    </tbody>
                </table>
                 {loading && <div className="p-8 text-center text-blue-500">Загрузка...</div>}
             </div>
        )}

      </main>
    </div>
  );
}

function SidebarItem({ icon, label, active, onClick }) {
  return (
    <button 
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
        active 
          ? 'bg-blue-50 text-blue-700 font-medium' 
          : 'text-gray-600 hover:bg-gray-50'
      }`}
    >
      {React.cloneElement(icon, { size: 20 })}
      <span>{label}</span>
    </button>
  );
}

function StatCard({ title, value }) {
    return (
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h3 className="text-gray-500 text-sm font-medium mb-2 uppercase tracking-wide">{title}</h3>
            <div className="text-4xl font-bold text-gray-900">{value}</div>
        </div>
    )
}

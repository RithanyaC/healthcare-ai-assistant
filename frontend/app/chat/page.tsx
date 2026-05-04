import ChatBox from '@/components/ChatBox';

export const metadata = {
  title: 'Consultation | Healthcare AI',
};

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center pt-10 pb-4 px-4 font-sans text-white">
      {/* Background Gradients */}
      <div className="fixed top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
        <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] rounded-full bg-blue-600/10 blur-[100px]"></div>
        <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] rounded-full bg-purple-600/10 blur-[100px]"></div>
      </div>
      
      <div className="w-full max-w-4xl z-10 flex flex-col h-[calc(100vh-4rem)]">
        <header className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
              Healthcare Assistant
            </h1>
            <p className="text-sm text-slate-400">Multi-agent orchestration system</p>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
            <span className="text-sm text-slate-400 font-medium">System Online</span>
          </div>
        </header>
        
        <main className="flex-1 bg-slate-900/60 backdrop-blur-xl border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col">
          <ChatBox />
        </main>
      </div>
    </div>
  );
}

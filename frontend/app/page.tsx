import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center relative overflow-hidden font-sans text-white">
      {/* Background Gradients */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
        <div className="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] rounded-full bg-blue-600/20 blur-[120px]"></div>
        <div className="absolute top-[60%] -right-[10%] w-[40%] h-[60%] rounded-full bg-purple-600/20 blur-[120px]"></div>
      </div>

      <div className="z-10 text-center max-w-3xl px-6">
        <div className="mb-6 inline-block">
          <span className="px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium tracking-wide">
            Next-Gen Healthcare AI
          </span>
        </div>
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-8">
          Intelligent Care, <br/>
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
            Delivered Instantly.
          </span>
        </h1>
        <p className="text-slate-400 text-lg md:text-xl mb-12 max-w-2xl mx-auto leading-relaxed">
          Experience the future of medical assistance. Our multi-agent AI system provides instant triage, seamless scheduling, and comprehensive medical summaries with enterprise-grade reliability.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link href="/chat" className="px-8 py-4 rounded-full bg-white text-slate-900 font-semibold text-lg hover:bg-slate-100 transition-all duration-300 transform hover:scale-105 hover:shadow-[0_0_20px_rgba(255,255,255,0.3)]">
            Start Consultation
          </Link>
          <a href="#features" className="px-8 py-4 rounded-full bg-slate-800/50 text-white font-semibold text-lg border border-slate-700 hover:bg-slate-800 transition-all duration-300">
            Learn More
          </a>
        </div>
      </div>

      {/* Feature Pills */}
      <div className="absolute bottom-10 z-10 flex flex-wrap justify-center gap-4 px-4 opacity-80">
        <div className="flex items-center gap-2 bg-slate-900/50 backdrop-blur-md px-4 py-2 rounded-full border border-slate-800">
          <div className="w-2 h-2 rounded-full bg-green-400"></div>
          <span className="text-sm font-medium">Smart Triage</span>
        </div>
        <div className="flex items-center gap-2 bg-slate-900/50 backdrop-blur-md px-4 py-2 rounded-full border border-slate-800">
          <div className="w-2 h-2 rounded-full bg-blue-400"></div>
          <span className="text-sm font-medium">Auto Scheduling</span>
        </div>
        <div className="flex items-center gap-2 bg-slate-900/50 backdrop-blur-md px-4 py-2 rounded-full border border-slate-800">
          <div className="w-2 h-2 rounded-full bg-purple-400"></div>
          <span className="text-sm font-medium">EHR Integration</span>
        </div>
      </div>
    </div>
  );
}

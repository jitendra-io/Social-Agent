import React, { useState } from 'react'
import { 
  CheckCircle, 
  MessageCircle, 
  ArrowRight, 
  Star, 
  ShieldCheck, 
  Zap, 
  ChevronRight,
  Menu,
  X,
  PhoneCall,
  Mail,
  Clock
} from 'lucide-react'

export default function App() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const featuresList = [
  "Single-Origin Ethical Sourcing",
  "Small Batch Drum Roasting",
  "Same-Day Courier Delivery",
  "Wholesale Commercial Supply"
]

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans relative overflow-x-hidden">
      {/* Background Decorative Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] glow-gradient pointer-events-none -z-10" />

      {/* Navigation Header */}
      <nav className="glass-nav sticky top-0 z-50 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center font-black text-xl text-white shadow-lg shadow-indigo-500/25">
              B
            </div>
            <div>
              <span className="font-bold text-xl tracking-tight text-white">BrewLab Specialty Roastery</span>
              <span className="block text-xs text-indigo-400 font-medium">Artisan Coffee & Retail</span>
            </div>
          </div>

          {/* Desktop Nav Links */}
          <div className="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-300">
            <a href="#services" className="hover:text-white transition-colors">Services</a>
            <a href="#why-us" className="hover:text-white transition-colors">Why Us</a>
            <a href="#pricing" className="hover:text-white transition-colors">Pricing</a>
            <a 
              href="https://wa.me/14155552671?text=Hello%20BrewLab Specialty Roastery,%20I%20am%20interested%20in%20your%20services!" 
              target="_blank" 
              rel="noopener noreferrer"
              className="px-5 py-2.5 rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-semibold flex items-center space-x-2 shadow-lg shadow-emerald-500/20 hover:shadow-emerald-500/40 hover:scale-105 transition-all duration-200"
            >
              <MessageCircle className="w-4 h-4" />
              <span>WhatsApp Us</span>
            </a>
          </div>

          {/* Mobile Menu Toggle */}
          <button 
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden text-slate-400 hover:text-white focus:outline-none"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Dropdown */}
        {mobileMenuOpen && (
          <div className="md:hidden mt-4 pt-4 border-t border-slate-800 space-y-3 pb-2 text-center">
            <a href="#services" onClick={() => setMobileMenuOpen(false)} className="block py-2 text-slate-300 hover:text-white">Services</a>
            <a href="#why-us" onClick={() => setMobileMenuOpen(false)} className="block py-2 text-slate-300 hover:text-white">Why Us</a>
            <a href="#pricing" onClick={() => setMobileMenuOpen(false)} className="block py-2 text-slate-300 hover:text-white">Pricing</a>
            <a 
              href="https://wa.me/14155552671?text=Hello%20BrewLab Specialty Roastery,%20I%20am%20interested%20in%20your%20services!" 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-2 px-6 py-2.5 rounded-full bg-emerald-500 text-white font-semibold shadow-md"
            >
              <MessageCircle className="w-4 h-4" />
              <span>Chat on WhatsApp</span>
            </a>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <header className="relative pt-24 pb-20 px-6 max-w-5xl mx-auto text-center flex-1">
        <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full bg-indigo-950/80 border border-indigo-700/40 text-indigo-300 text-xs font-semibold mb-8 animate-pulse">
          <Zap className="w-3.5 h-3.5 text-indigo-400" />
          <span>Premier Artisan Coffee & Retail Solutions</span>
        </div>

        <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight text-white mb-6 leading-tight">
          Obsessively Sourced, Precision Roasted Daily
        </h1>

        <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
          Experience world-class quality with instant customer service. We deliver end-to-end satisfaction customized for your exact requirements.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="https://wa.me/14155552671?text=Hello%20BrewLab Specialty Roastery,%20I%20am%20interested%20in%20your%20services!"
            target="_blank"
            rel="noopener noreferrer"
            className="w-full sm:w-auto px-8 py-4 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-bold text-base flex items-center justify-center space-x-3 shadow-xl shadow-emerald-500/25 hover:shadow-emerald-500/40 hover:-translate-y-0.5 transition-all duration-200"
          >
            <MessageCircle className="w-5 h-5" />
            <span>Connect on WhatsApp</span>
            <ArrowRight className="w-4 h-4 ml-1" />
          </a>
          <a
            href="#services"
            className="w-full sm:w-auto px-8 py-4 rounded-xl glass-panel text-slate-200 font-semibold text-base hover:bg-slate-800/80 transition-colors"
          >
            Explore Offerings
          </a>
        </div>

        {/* Social Proof Badges */}
        <div className="mt-14 pt-10 border-t border-slate-800/60 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div>
            <p className="text-2xl font-bold text-white">99.8%</p>
            <p className="text-xs text-slate-400 mt-1">Satisfaction Rate</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-white">24 / 7</p>
            <p className="text-xs text-slate-400 mt-1">Instant Support</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-white">100%</p>
            <p className="text-xs text-slate-400 mt-1">Verified Guarantee</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-white">Top Rated</p>
            <p className="text-xs text-slate-400 mt-1">In Industry</p>
          </div>
        </div>
      </header>

      {/* Offerings Section */}
      <section id="services" className="py-20 px-6 bg-slate-900/50 relative border-t border-slate-800/80">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Core Capabilities</h2>
            <p className="text-slate-400 max-w-xl mx-auto text-sm md:text-base">
              Designed and executed with obsessive attention to detail, tailored specifically for BrewLab Specialty Roastery.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuresList.map((item, index) => (
              <div 
                key={index} 
                className="glass-panel p-8 rounded-2xl hover:border-indigo-500/40 hover:-translate-y-1 transition-all duration-300 relative group"
              >
                <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-6 group-hover:scale-110 group-hover:bg-indigo-500 group-hover:text-white transition-all duration-200">
                  <ShieldCheck className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold text-white mb-2">{item}</h3>
                <p className="text-slate-400 text-sm leading-relaxed mb-6">
                  Engineered for seamless efficiency and peak operational impact with direct verification.
                </p>
                <a 
                  href="https://wa.me/14155552671?text=Hello%20BrewLab Specialty Roastery,%20I%20am%20interested%20in%20your%20services!" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-indigo-400 text-sm font-semibold flex items-center group-hover:text-indigo-300"
                >
                  <span>Inquire Now</span>
                  <ChevronRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                </a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Interactive WhatsApp Direct Action Section */}
      <section className="py-20 px-6 max-w-4xl mx-auto text-center">
        <div className="glass-panel p-10 md:p-14 rounded-3xl border border-indigo-500/30 relative overflow-hidden">
          <div className="w-16 h-16 rounded-2xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 mx-auto mb-6">
            <PhoneCall className="w-8 h-8" />
          </div>
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Ready To Get Started?</h2>
          <p className="text-slate-400 max-w-xl mx-auto mb-8 text-sm md:text-base">
            Skip bureaucratic email threads. Speak directly with the BrewLab Specialty Roastery leadership team via WhatsApp right now.
          </p>
          <a
            href="https://wa.me/14155552671?text=Hello%20BrewLab Specialty Roastery,%20I%20am%20interested%20in%20your%20services!"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-3 px-8 py-4 rounded-xl bg-emerald-500 text-white font-bold text-lg shadow-xl shadow-emerald-500/25 hover:bg-emerald-400 hover:scale-105 transition-all duration-200"
          >
            <MessageCircle className="w-6 h-6" />
            <span>Open WhatsApp Chat</span>
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto py-10 px-6 border-t border-slate-900 bg-slate-950 text-slate-500 text-xs text-center">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <p>© {new Date().getFullYear()} BrewLab Specialty Roastery. All rights reserved.</p>
          <p className="text-slate-600">Built autonomously with modern React, Tailwind CSS & Google Antigravity.</p>
        </div>
      </footer>

      {/* Persistent Floating WhatsApp Floating Action Button */}
      <a
        href="https://wa.me/14155552671?text=Hello%20BrewLab Specialty Roastery,%20I%20am%20interested%20in%20your%20services!"
        target="_blank"
        rel="noopener noreferrer"
        aria-label="Direct WhatsApp Contact"
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-emerald-500 hover:bg-emerald-400 text-white flex items-center justify-center shadow-2xl shadow-emerald-500/50 hover:scale-110 active:scale-95 transition-all duration-200 group"
      >
        <MessageCircle className="w-7 h-7" />
        <span className="sr-only">Chat with us</span>
      </a>
    </div>
  )
}

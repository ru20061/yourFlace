"use client";

import { useState } from "react";
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import Sidebar from "./components/Sidebar/Sidebar";

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="app-layout">
      <Header
        isAdmin={false}
        isLoggedIn={false}
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
      />
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        isAdmin={false}
        subscribedArtists={[]}
      />
      <main className="app-main">
        {children}
      </main>
      <Footer isSubscribed={false} isAdmin={false} />
    </div>
  );
}

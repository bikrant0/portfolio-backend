import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css';
import Navbar from './components/Navbar';

export default function App(){
  return(
    <div>
      <Navbar />
      <main>
      <h1>Backend Engineering Portfolio</h1>
      <p>
        Proving backend stability, relational integrity, and secure API architecture through real-time integration.
      </p>
      </main>
    </div>
  )
}



import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import PromotionsList from './PromotionsList';

function App() {
  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold">Promo-Finder MVP</h1>
      </header>
      <PromotionsList />
    </div>
  );
}

export default App;

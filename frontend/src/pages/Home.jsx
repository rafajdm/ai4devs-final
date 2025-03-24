import React, { useState } from "react";
import MenuToolbar from "../components/MenuToolbar";
import SearchFilters from "../components/SearchFilters";
import PromotionsCarousel from "../components/PromotionsCarousel";
import Footer from "../components/Footer";

const Home = () => {
  const [filters, setFilters] = useState({});
  
  const handleApplyFilters = (restaurantName, region) => {
    setFilters({ restaurantName, region });
  };

  const handleClearFilters = () => setFilters({});
  
  return (
    <div className="min-h-screen flex flex-col pt-[calc(50px+64px)]">
      <MenuToolbar />
      <SearchFilters 
        onApplyFilters={handleApplyFilters} 
        onClearFilters={handleClearFilters} 
      />
      <div className="flex-grow">
        <PromotionsCarousel filters={filters} />
      </div>
      <Footer />
    </div>
  );
};

export default Home;

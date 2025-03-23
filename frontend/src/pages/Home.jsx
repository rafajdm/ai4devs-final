import React from 'react';
import MenuToolbar from '../components/MenuToolbar';
import SearchFilters from '../components/SearchFilters';
import PromotionsCarousel from '../components/PromotionsCarousel';
import Footer from '../components/Footer';

const Home = () => {
    return (
        <div className="min-h-screen flex flex-col">
            <MenuToolbar />
            <SearchFilters />
            <div className="flex-grow">
                <PromotionsCarousel />
            </div>
            <Footer />
        </div>
    );
};

export default Home;

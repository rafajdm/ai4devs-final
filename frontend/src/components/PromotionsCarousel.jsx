import React, { useState, useEffect } from 'react';
import Slider from 'react-slick';
import PromotionCard from './PromotionCard';

// IMPORTANT: Import the slick-carousel CSS so styles are applied
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const INITIAL_PAGE = 1;
const PAGE_SIZE = 10;

const PromotionsCarousel = () => {
    const [promotions, setPromotions] = useState([]);
    const [page, setPage] = useState(INITIAL_PAGE);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);

    // Load promotions from your backend API
    const loadPromotions = async (pageNumber) => {
        setLoading(true);
        try {
            const res = await fetch(`${import.meta.env.VITE_API_URL}/promotions?page=${pageNumber}&page_size=${PAGE_SIZE}`);
            const data = await res.json();
            setPromotions((prev) => [...prev, ...data]);
            setPage(pageNumber);
            if (data.length < PAGE_SIZE) {
                setHasMore(false);
            }
        } catch (err) {
            console.error('Failed to load promotions', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadPromotions(INITIAL_PAGE);
    }, []);

    const settings = {
        dots: true,
        infinite: false,
        speed: 500,
        slidesToShow: 3,   // Show 3 cards on screens >=1024px
        slidesToScroll: 1,
        lazyLoad: 'ondemand',
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 2
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1
                }
            }
        ],
        afterChange: (current) => {
            if (!loading && hasMore && current >= promotions.length - 4) {
                loadPromotions(page + 1);
            }
        }
    };

    return (
        <div className="max-w-5xl mx-auto py-8 px-4 bg-gray-100 border-4 border-blue-500">
            <Slider {...settings}>
                {promotions.map((promo) => (
                    <div key={promo.id} className="px-2">
                        <PromotionCard promotion={promo} />
                    </div>
                ))}
            </Slider>
        </div>
    );
};

export default PromotionsCarousel;
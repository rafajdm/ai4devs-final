import React, { useState, useEffect } from 'react';
import Slider from 'react-slick';
import PromotionCard from './PromotionCard';

const INITIAL_PAGE = 1;
const PAGE_SIZE = 10; // increased number of promotions per fetch

const PromotionsCarousel = () => {
    const [promotions, setPromotions] = useState([]);
    const [page, setPage] = useState(INITIAL_PAGE);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true); // track if more promotions exist

    // Function to load promotions from our backend API (dockerized env)
    const loadPromotions = async (pageNumber) => {
        setLoading(true);
        try {
            const res = await fetch(`${import.meta.env.VITE_API_URL}/promotions?page=${pageNumber}&page_size=${PAGE_SIZE}`);
            const data = await res.json();
            // If API doesn't support pagination, you can simulate slicing.
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
        slidesToShow: 3,
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
            // Pre-fetch new promotions when nearing the end (e.g. within 4 slides) and if available.
            if (!loading && hasMore && current >= promotions.length - 4) {
                loadPromotions(page + 1);
            }
        }
    };

    return (
        <div className="w-full py-8 px-4 bg-gray-100">
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
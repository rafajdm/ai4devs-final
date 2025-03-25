import React, { useState, useEffect } from "react";
import Slider from "react-slick";
import PromotionCard from "./PromotionCard";

import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

const INITIAL_PAGE = 1;
const PAGE_SIZE = 10;

const PromotionsCarousel = ({ filters }) => {
  const [promotions, setPromotions] = useState([]);
  const [page, setPage] = useState(INITIAL_PAGE);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [sliderRef, setSliderRef] = useState(null);

  const loadPromotions = async (pageNumber) => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        page: pageNumber,
        page_size: PAGE_SIZE,
        ...(filters.restaurantName && {
          restaurant_name: filters.restaurantName,
        }),
        ...(filters.region && { region: filters.region }),
      });
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/promotions/?${params.toString()}`
      );
      const data = await res.json();
      setPromotions((prev) => [...prev, ...data]);
      setPage(pageNumber);
      if (data.length < PAGE_SIZE) {
        setHasMore(false);
      }
    } catch (err) {
      console.error("Failed to load promotions", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPromotions(INITIAL_PAGE);
  }, []);

  useEffect(() => {
    // Reset promotions when filters change
    setPromotions([]);
    setPage(INITIAL_PAGE);
    setHasMore(true);
    loadPromotions(INITIAL_PAGE);
  }, [filters]);

  const handlePrevious = () => {
    if (sliderRef) {
      sliderRef.slickPrev();
    }
  };

  const handleNext = () => {
    if (sliderRef) {
      sliderRef.slickNext();
    }
  };

  const settings = {
    dots: false,
    infinite: false,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    lazyLoad: "progressive",
    nextArrow: (
      <div className="text-4xl text-gray-100 bg-black/60 hover:bg-gray-700 w-10 h-10 flex items-center justify-center rounded-full cursor-pointer absolute right-2 md:right-4 top-1/2 transform -translate-y-1/2 z-50 shadow-lg opacity-90">
        {">"}
      </div>
    ),
    prevArrow: (
      <div className="text-4xl text-gray-100 bg-black/60 hover:bg-gray-700 w-10 h-10 flex items-center justify-center rounded-full cursor-pointer absolute left-2 md:left-4 top-1/2 transform -translate-y-1/2 z-50 shadow-lg opacity-90">
        {"<"}
      </div>
    ),
    responsive: [
      {
        breakpoint: 1280,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          arrows: true, // Show arrows on mobile
          centerMode: true,
          centerPadding: "8px",
        },
      },
    ],
    afterChange: (current) => {
      if (!loading && hasMore && current >= promotions.length - 4) {
        loadPromotions(page + 1);
      }
    },
    ref: (slider) => setSliderRef(slider),
  };

  return (
    <div className="w-full md:max-w-screen-xl mx-auto py-2 md:py-4 px-0 md:px-8 mt-8 md:mt-20 mb-16 overflow-x-hidden relative">
      {/* Clickable minimal indicators */}
      <span
        onClick={handlePrevious}
        className="md:hidden absolute left-2 top-1/2 -translate-y-1/2 z-10 text-white/80 text-3xl hover:text-white transition-colors cursor-pointer select-none"
      >
        &lt;
      </span>
      <span
        onClick={handleNext}
        className="md:hidden absolute right-2 top-1/2 -translate-y-1/2 z-10 text-white/80 text-3xl hover:text-white transition-colors cursor-pointer select-none"
      >
        &gt;
      </span>

      {loading && promotions.length === 0 ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : promotions.length === 0 ? (
        <div className="text-center text-gray-600 py-12">
          No promotions found with the current filters
        </div>
      ) : (
        <Slider {...settings}>
          {promotions.map((promo) => (
            <div key={promo.id} className="px-1 md:px-2">
              <PromotionCard promotion={promo} />
            </div>
          ))}
        </Slider>
      )}
      {loading && promotions.length > 0 && (
        <div className="text-center py-4">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      )}
    </div>
  );
};

export default PromotionsCarousel;

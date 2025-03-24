import React, { useState, useEffect } from "react";
import Slider from "react-slick";
import PromotionCard from "./PromotionCard";

import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

const INITIAL_PAGE = 1;
const PAGE_SIZE = 10;

const PromotionsCarousel = () => {
  const [promotions, setPromotions] = useState([]);
  const [page, setPage] = useState(INITIAL_PAGE);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  const loadPromotions = async (pageNumber) => {
    setLoading(true);
    try {
      const res = await fetch(
        `${
          import.meta.env.VITE_API_URL
        }/promotions?page=${pageNumber}&page_size=${PAGE_SIZE}`
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

  const settings = {
    dots: false,
    infinite: false,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    lazyLoad: "progressive",
    nextArrow: (
      <div className="text-8xl text-gray-100 bg-black/60 hover:bg-gray-700 w-12 h-12 flex items-center justify-center rounded-full cursor-pointer absolute right-6 top-1/2 transform -translate-y-1/2 z-50 shadow-lg opacity-90">
        {">"}
      </div>
    ),
    prevArrow: (
      <div className="text-8xl text-gray-100 bg-black/60 hover:bg-gray-700 w-12 h-12 flex items-center justify-center rounded-full cursor-pointer absolute left-6 top-1/2 transform -translate-y-1/2 z-50 shadow-lg opacity-90">
        {"<"}
      </div>
    ),
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 2,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1,
        },
      },
    ],
    afterChange: (current) => {
      if (!loading && hasMore && current >= promotions.length - 4) {
        loadPromotions(page + 1);
      }
    },
  };

  return (
    <div className="w-full max-w-screen-xl mx-auto py-8 px-8 mt-10 overflow-x-hidden">
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

import React from "react";

const PromotionCard = ({ promotion }) => {
  return (
    <div className="bg-gray-800 text-white shadow-lg rounded-lg p-6 border border-gray-700 border-2 border-yellow-500 h-48 flex flex-col">
      {/* Restaurant Name as Header */}
      <h2 className="text-xl font-bold text-center pb-2 border-b border-gray-600">
        {promotion.restaurant_name}
      </h2>

      {/* Content Wrapper */}
      <div className="flex flex-row items-center pt-2">
        {/* Logo Section */}
        <div className="flex-shrink-0 w-20 h-20 flex items-center justify-center">
          {promotion.logo_path && (
            <img
              src={`${import.meta.env.VITE_API_URL}/${promotion.logo_path}`}
              alt={`${promotion.restaurant_name} logo`}
              className="w-full h-full object-contain"
            />
          )}
        </div>

        {/* Details Section */}
        <div className="flex-grow ml-4 text-left">
          <p className="mb-1">
            <strong>Discount:</strong> {promotion.discount_rate ?? "N/A"}
          </p>
          <p className="mt-1">
            <strong>Validity:</strong> {promotion.valid_period_text ?? "N/A"}
          </p>
        </div>
      </div>
    </div>
  );
};

export default PromotionCard;

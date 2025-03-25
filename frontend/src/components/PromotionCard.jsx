import React from "react";

const PromotionCard = ({ promotion }) => {
  return (
    <div
      className="bg-gray-800 text-white shadow-lg rounded-lg p-6 border border-gray-700 border-2 border-yellow-500
      md:h-48 min-h-[364px] md:min-h-[200px] flex flex-col justify-between mx-auto max-w-[95%] md:max-w-full"
    >
      <h2 className="text-xl md:text-xl font-bold text-center pb-3 border-b border-gray-600">
        {promotion.restaurant_name}
      </h2>

      <div className="flex flex-row items-center flex-grow pt-6 md:pt-4">
        <div className="flex-shrink-0 w-24 md:w-20 h-24 md:h-20 flex items-center justify-center">
          {promotion.logo_path && (
            <img
              src={`${import.meta.env.VITE_API_URL}/${promotion.logo_path}`}
              alt={`${promotion.restaurant_name} logo`}
              className="w-full h-full object-contain"
            />
          )}
        </div>

        <div className="flex-grow ml-6 md:ml-4 text-left">
          <p className="mb-4 md:mb-2 text-base">
            <strong>Descuento:</strong> {promotion.discount_rate ?? "N/A"}
          </p>
          <p className="text-base">
            <strong>Validez:</strong> {promotion.valid_period_text ?? "N/A"}
          </p>
        </div>
      </div>
    </div>
  );
};

export default PromotionCard;

import React from 'react';

const PromotionCard = ({ promotion }) => {
  return (
    <div className="bg-gray-800 text-white shadow-lg rounded-lg p-6 border border-gray-700 border-2 border-yellow-500">
      <h2 className="text-xl font-bold mb-2">{promotion.restaurant_name}</h2>
      {promotion.logo_path && (
        <img
          src={`${import.meta.env.VITE_API_URL}/${promotion.logo_path}`}
          alt={`${promotion.restaurant_name} logo`}
          className="w-full h-32 object-contain mb-4"
        />
      )}
      <p className="mb-1"><strong>Discount:</strong> {promotion.discount_rate ?? 'N/A'}</p>
      <p className="mb-1"><strong>Validity:</strong> {promotion.valid_period_text ?? 'N/A'}</p>
    </div>
  );
};

export default PromotionCard;
import React, { useState, useEffect } from 'react';

const PromotionsList = () => {
  const [promotions, setPromotions] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/promotions')
      .then(response => response.json())
      .then(data => setPromotions(data))
      .catch(error => console.error('Error fetching promotions:', error));
  }, []);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {promotions.map(promo => (
        <div key={promo.id} className="bg-gray-800 text-white shadow-lg rounded-lg p-6 border border-gray-700">
          <h2 className="text-xl font-bold mb-2">{promo.restaurant_name}</h2>
          {promo.logo_path && (
            <img src={`http://localhost:8000/${promo.logo_path}`} alt={`${promo.restaurant_name} logo`} className="w-full h-32 object-contain mb-4"/>
          )}
          <p className="mb-1"><strong>Discount:</strong> {promo.discount_rate ?? 'N/A'}</p>
          <p className="mb-1"><strong>Valid Days:</strong> {promo.applicable_days_text ?? 'N/A'}</p>
          <p className="mb-1"><strong>Address:</strong> {promo.address ?? 'N/A'}</p>
          <p className="mb-1"><strong>Validity:</strong> {promo.valid_period_text ?? 'N/A'}</p>
          {promo.valid_from && promo.valid_until && (
            <p className="mb-1">
              <strong>From:</strong> {new Date(promo.valid_from).toLocaleDateString()} {" "}
              <strong>Until:</strong> {new Date(promo.valid_until).toLocaleDateString()}
            </p>
          )}
          <p className="mb-1"><strong>Source:</strong> {promo.source ?? 'N/A'}</p>
          <p className="mb-1"><strong>Region:</strong> {promo.region ?? 'N/A'}</p>
          <p className="mb-1"><strong>AI Summary:</strong> {promo.ai_summary ?? 'N/A'}</p>
          <p className="text-sm text-gray-500">
            {promo.created_at ? new Date(promo.created_at).toLocaleString() : ''}
          </p>
        </div>
      ))}
    </div>
  );
};

export default PromotionsList;

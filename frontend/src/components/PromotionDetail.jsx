import React, { useState } from "react";
import { createPortal } from "react-dom";
import { usePromotion } from "../hooks/usePromotion";

const DaysOfWeek = ({ daysString }) => {
  const days = ['D', 'L', 'M', 'M', 'J', 'V', 'S'];
  const activeDays = daysString ? daysString.split(',').map(Number) : [];

  return (
    <div className="flex gap-1">
      {days.map((day, index) => {
        const adjustedIndex = index === 0 ? 0 : index;
        const isActive = activeDays.includes(adjustedIndex);
        return (
          <div
            key={index}
            className={`w-8 h-8 border border-gray-500 flex items-center justify-center rounded 
              ${isActive ? 'bg-blue-500 text-white' : 'text-gray-400'}`}
          >
            {day}
          </div>
        );
      })}
    </div>
  );
};

const PromotionDetail = ({ promotionId, onClose, isOpen }) => {
  const { promotion, loading, error, mutate } = usePromotion(isOpen ? promotionId : null);
  const [updating, setUpdating] = useState(false);
  const [updateMessage, setUpdateMessage] = useState(null);

  const handleUpdate = async () => {
    try {
      setUpdating(true);
      setUpdateMessage(null);

      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/ai-process/${promotionId}`, {
        method: 'POST',
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to update promotion');
      }

      setUpdateMessage({ type: 'success', text: 'Promotion updated successfully!' });
      
      // Only call mutate if it exists
      if (typeof mutate === 'function') {
        await mutate();
      }
    } catch (error) {
      console.error('Error updating promotion:', error);
      setUpdateMessage({ type: 'error', text: error.message });
    } finally {
      setUpdating(false);
    }
  };

  if (!isOpen) return null;

  return createPortal(
    <>
      <div className="fixed inset-0 bg-black/50 z-[100]" onClick={onClose} />
      <div className={`fixed z-[101] bg-gray-800 text-white
          md:w-[40%] md:right-0 md:top-0 md:h-full
          w-full h-screen top-0 left-0
          transform transition-transform duration-300 ease
          ${isOpen ? "translate-x-0" : "translate-x-full"}
          overflow-y-auto`}
      >
        <div className="flex flex-col h-full p-6">
          <div className="flex flex-col gap-4 mb-4">
            {updateMessage && (
              <div className={`p-2 rounded ${
                updateMessage.type === 'success' ? 'bg-green-600' : 'bg-red-600'
              }`}>
                {updateMessage.text}
              </div>
            )}
            <div className="flex justify-between items-center">
              <button
                onClick={handleUpdate}
                disabled={updating}
                className="px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-md disabled:opacity-50"
              >
                {updating ? 'Actualizando...' : 'Actualizar (AI)'}
              </button>
              <button onClick={onClose} className="text-gray-400 hover:text-white">
                ✕
              </button>
            </div>
          </div>

          {loading && <p className="text-center">Loading...</p>}
          {error && <p className="text-red-500 text-center">{error}</p>}
          
          {promotion && (
            <>
              <h2 className="text-2xl font-bold mb-6 border-b border-gray-600 pb-3">
                {promotion.restaurant_name}
              </h2>

              <div className="hidden md:block mb-6">
                {promotion.logo_path && (
                  <img
                    src={`${import.meta.env.VITE_API_URL}/scraped_data/${promotion.logo_path.replace('scraped_data/', '')}`}
                    alt={`${promotion.restaurant_name} logo`}
                    className="w-48 h-48 object-contain mx-auto"
                  />
                )}
              </div>

              <div className="space-y-4">
                <p><strong>Descuento:</strong> {promotion.discount_rate || "-"}</p>
                <p><strong>Validez:</strong> {promotion.valid_period_text ?? "N/A"}</p>
                <p><strong>Descripción:</strong> {promotion.applicable_days_text ?? "N/A"}</p>
                <p><strong>Dirección:</strong> {promotion.address ?? "N/A"}</p>
                <p><strong>Región:</strong> {promotion.region ?? "N/A"}</p>
                <p><strong>Válido hasta:</strong> {promotion.valid_until ? new Date(promotion.valid_until).toLocaleDateString('es-CL', { month: '2-digit', day: '2-digit', year: 'numeric' }) : "-"}</p>
                <p><strong>Fuente:</strong> {promotion.source ?? "N/A"}</p>
                {promotion.days_of_week && (
                  <div className="pt-4 border-t border-gray-600">
                    <strong>Días aplicables:</strong>
                    <div className="mt-2">
                      <DaysOfWeek daysString={promotion.days_of_week} />
                    </div>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </>,
    document.body
  );
};

export default PromotionDetail;

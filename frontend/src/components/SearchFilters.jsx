import React, { useState } from "react";

const SearchFilters = ({ onApplyFilters, onClearFilters }) => {
  const [restaurantName, setRestaurantName] = useState("");
  const [region, setRegion] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const toggleFilters = () => setIsOpen(!isOpen);

  const handleApply = () => {
    onApplyFilters(restaurantName, region);
    setIsOpen(false);
  };

  const handleClear = () => {
    setRestaurantName("");
    setRegion("");
    onClearFilters();
    setIsOpen(false);
  };

  return (
    <>
      {/* Mobile Toggle Button */}
      <button
        className="md:hidden fixed top-[70px] right-4 z-20 bg-blue-600 text-white p-2 rounded-md shadow-lg"
        onClick={toggleFilters}
      >
        {isOpen ? "Cerrar Filtros" : "Ver Filtros"}
      </button>

      {/* Filters Container - Fixed toolbar on desktop, overlay on mobile */}
      <div
        className={`
          md:fixed md:top-[50px] md:left-0 md:right-0 md:h-24 md:bg-gray-300 md:border-b md:border-gray-500 md:z-10
          fixed inset-0 bg-gray-300 z-20 md:translate-x-0
          ${isOpen ? "translate-x-0" : "-translate-x-full"}
          transition-transform duration-300 ease-in-out
        `}
      >
        <div className="flex md:flex-row flex-col md:items-center items-start md:justify-center gap-6 p-8 md:p-4 h-full">
          <span className="text-gray-900 font-medium text-lg">Filtros:</span>
          <input
            type="text"
            placeholder="Nombre del Restaurante"
            className="px-4 py-3 border border-gray-500 rounded-md text-gray-900 bg-white md:w-1/4 w-full"
            value={restaurantName}
            onChange={(e) => setRestaurantName(e.target.value)}
          />
          <select
            className="px-4 py-3 border border-gray-500 rounded-md text-gray-900 bg-white md:w-1/5 w-full h-12 appearance-none"
            value={region}
            onChange={(e) => setRegion(e.target.value)}
          >
            <option value="">Todas</option>
            <option value="Metropolitana">Metropolitana</option>
            <option value="Bío-Bío">Bío-Bío</option>
            <option value="Antofagasta">Antofagasta</option>
            <option value="Tarapacá">Tarapacá</option>
            <option value="Maule, Metropolitana">Maule, Metropolitana</option>
            <option value="Valparaíso">Valparaíso</option>
          </select>
          <label className="flex items-center space-x-2 text-gray-900 text-lg">
            <input
              type="checkbox"
              disabled
              className="form-checkbox text-gray-600"
            />
            <span>Aplica Hoy (Deshabilitado)</span>
          </label>
          <div className="flex md:flex-row flex-col gap-4 md:w-auto w-full">
            <button
              className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition text-lg"
              onClick={handleApply}
            >
              Aplicar
            </button>
            <button
              className="px-6 py-3 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition text-lg"
              onClick={handleClear}
            >
              Limpiar
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default SearchFilters;

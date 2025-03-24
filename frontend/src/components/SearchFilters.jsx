import React, { useState } from "react";

const SearchFilters = ({ onApplyFilters, onClearFilters }) => {
  const [restaurantName, setRestaurantName] = useState("");
  const [region, setRegion] = useState("");

  return (
    <div className="absolute top-[50px] left-0 right-0 w-full bg-gray-300 py-6 px-8 border-b border-gray-500 flex items-center justify-center gap-6 h-24 z-10">
      <span className="text-gray-900 font-medium text-lg">Search Filters:</span>
      <input
        type="text"
        placeholder="Restaurant Name"
        className="px-4 py-3 border border-gray-500 rounded-md text-gray-900 bg-white w-1/4"
        value={restaurantName}
        onChange={(e) => setRestaurantName(e.target.value)}
      />
      <select
        className="px-4 py-3 border border-gray-500 rounded-md text-gray-900 bg-white w-1/5"
        value={region}
        onChange={(e) => setRegion(e.target.value)}
      >
        <option value="">All</option>
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
        <span>Applies Today (Disabled)</span>
      </label>
      {/* New Buttons */}
      <button
        className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition text-lg"
        onClick={() => onApplyFilters(restaurantName, region)}
      >
        Apply
      </button>
      <button
        className="px-6 py-3 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition text-lg"
        onClick={() => {
          setRestaurantName("");
          setRegion("");
          onClearFilters();
        }}
      >
        Clear
      </button>
    </div>
  );
};

export default SearchFilters;

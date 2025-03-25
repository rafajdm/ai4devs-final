import useSWR from 'swr';

export function usePromotion(promotionId) {
  const { data, error, mutate } = useSWR(
    promotionId ? `/api/v1/promotions/${promotionId}` : null,
    async (url) => {
      const response = await fetch(`${import.meta.env.VITE_API_URL}${url}`);
      if (!response.ok) throw new Error('Failed to fetch promotion');
      return response.json();
    }
  );

  return {
    promotion: data,
    loading: !error && !data,
    error: error?.message,
    mutate
  };
}

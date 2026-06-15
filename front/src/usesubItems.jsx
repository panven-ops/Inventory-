import { useState, useCallback } from "react";
import { authFetch } from "./api";

export function useSubItems({ accessToken, refreshToken, setAccessToken, logout }) {
  const [subItemsMap, setSubItemsMap] = useState({});
  const [openCategories, setOpenCategories] = useState({});

  // Ανοίγει/κλείνει το accordion και φέρνει τα sub-items αν δεν τα έχει
  const toggleCategory = useCallback(async (categoryId) => {
    const isOpen = openCategories[categoryId];

    if (isOpen) {
      setOpenCategories((prev) => ({ ...prev, [categoryId]: false }));
      return;
    }

    // Αν δεν έχουμε ήδη τα sub-items, κάνε fetch
    if (!subItemsMap[categoryId]) {
      const res = await authFetch({
        url: `/items/${categoryId}/sub-items`,
        accessToken,
        refreshToken,
        setAccessToken,
        logout,
      });
      const data = await res.json();
      setSubItemsMap((prev) => ({ ...prev, [categoryId]: data }));
    }

    setOpenCategories((prev) => ({ ...prev, [categoryId]: true }));
  }, [openCategories, subItemsMap, accessToken, refreshToken, setAccessToken, logout]);

  const addSubItem = async (categoryId, name) => {
    const res = await authFetch({
      url: `/items/${categoryId}/sub-items`,
      method: "POST",
      body: { name, quantity: 0 },
      accessToken,
      refreshToken,
      setAccessToken,
      logout,
    });
    const data = await res.json();
    setSubItemsMap((prev) => ({
      ...prev,
      [categoryId]: [...(prev[categoryId] || []), data],
    }));
  };

  const deleteSubItem = async (categoryId, subItemId) => {
    setSubItemsMap((prev) => ({
      ...prev,
      [categoryId]: prev[categoryId].filter((s) => s.id !== subItemId),
    }));
    await authFetch({
      url: `/items/${categoryId}/sub-items/${subItemId}`,
      method: "DELETE",
      accessToken,
      refreshToken,
      setAccessToken,
      logout,
    });
  };

  const updateQuantity = async (categoryId, subItemId, newQuantity) => {
    // Αν πάει κάτω από 0, σταμάτα
    if (newQuantity < 0) return;

    // Optimistic update — αλλάζει αμέσως στο UI
    setSubItemsMap((prev) => ({
      ...prev,
      [categoryId]: prev[categoryId].map((s) =>
        s.id === subItemId ? { ...s, quantity: newQuantity } : s
      ),
    }));

    await authFetch({
      url: `/items/${categoryId}/sub-items/${subItemId}/quantity`,
      method: "PATCH",
      body: { quantity: newQuantity },
      accessToken,
      refreshToken,
      setAccessToken,
      logout,
    });
  };

  return {
    subItemsMap,
    openCategories,
    toggleCategory,
    addSubItem,
    deleteSubItem,
    updateQuantity,
  };
}

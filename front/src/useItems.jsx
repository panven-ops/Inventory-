import React, { useRef, useState, useEffect } from "react";
import { authFetch } from "./api";
import { useAuth } from "./AuthContext";

export function useItems() {
  const auth = useAuth() || {};

  const accessToken = auth.accessToken;
  const refreshToken = auth.refreshToken;
  const setAccessToken = auth.setAccessToken || (() => {});
  const logout = auth.logout || (() => {});
    if (!logout || !setAccessToken) {
      console.error("AuthContext missing functions", {
        setAccessToken,
        logout,
      });
    }
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState("");

  const [skip, setSkip] = useState(0);
  const [limit] = useState(10);
  const [total, setTotal] = useState(0);

  const cacheRef = useRef({});

  useEffect(() => {
    if (!accessToken) return;

    const cacheKey = `${skip}-${limit}`;

    const getItems = async () => {
      if (cacheRef.current[cacheKey]) {
        const cached = cacheRef.current[cacheKey];
        setItems(cached.data);
        setTotal(cached.total);
        return;
      }

      const res = await authFetch({
        url: `/items?skip=${skip}&limit=${limit}`,
        accessToken,
        refreshToken,
        setAccessToken,
        logout,
      });

      const data = await res.json();

      setItems(data.data);
      setTotal(data.total);

      cacheRef.current[cacheKey] = {
        data: data.data,
        total: data.total,
      };
    };

    getItems();
  }, [accessToken, skip, limit])

  const addItem = async () => {
    if (!newItem) return;

    const temp = { id: Date.now(), name: newItem };

    setItems((prev) => [...prev, temp]);
    setNewItem("");

    const res = await authFetch({
      url: "/items",
      method: "POST",
      body: { name: newItem },
      accessToken,
      refreshToken,
      setAccessToken,
      logout,
    });

    const data = await res.json();
    cacheRef.current = {};
    setItems((prev) =>
      prev.map((i) => (i.id === temp.id ? data : i)));
    setTotal((prev) => prev + 1);
  };

  const deleteItem = async (id) => {
    setItems((prev) => prev.filter((i) => i.id !== id));

    await authFetch({
      url: `/items/${id}`,
      method: "DELETE",
      accessToken,
      refreshToken,
      setAccessToken,
      logout,
    });
    cacheRef.current = {};
    setTotal((prev) => prev - 1);
  };

  const updateItem = async (id, name) => {
    const res = await authFetch({
      url: `/items/${id}`,
      method: "PUT",
      body: { name },
      accessToken,
      refreshToken,
      setAccessToken,
      logout,
    });

    const data = await res.json();
    cacheRef.current = {};
    setItems((prev) => prev.map((i) => (i.id === id ? data : i)));
  };

  return {
    items,
    newItem,
    setNewItem,
    addItem,
    deleteItem,
    updateItem,
    skip,
    setSkip,
    limit,
    total,
  };
}

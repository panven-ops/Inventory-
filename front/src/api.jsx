const API_URL = "http://localhost:8000";

/**
 * Refresh access token using refresh token
 */
export const refreshAccessToken = async (refresh_token) => {
  try {
    const res = await fetch(`${API_URL}/refresh`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${refresh_token}`,
      },
    });

    if (!res.ok) throw new Error("Refresh failed");

    const data = await res.json();
    return data.access_token;
  } catch (err) {
    console.error("REFRESH ERROR:", err);
    return null;
  }
};

/**
 * Main auth fetch wrapper
 * Handles:
 * - adding access token
 * - retry on 401 using refresh token
 */
export const authFetch = async ({
  url,
  method = "GET",
  body,
  accessToken,
  refreshToken,
  setAccessToken,
  logout,
}) => {
  // 1st request
  let res = await fetch(`${API_URL}${url}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  // If token expired → refresh
  if (res.status === 401) {
    const newAccessToken = await refreshAccessToken(refreshToken);

    if (!newAccessToken) {
      logout?.();
      return res;
    }
    if (setAccessToken) {
      setAccessToken(newAccessToken);
    }

    // update state in React
    setAccessToken(newAccessToken);
    localStorage.setItem("access_token", newAccessToken);

    // retry request with new token
    res = await fetch(`${API_URL}${url}`, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${newAccessToken}`,
      },
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  return res;
};

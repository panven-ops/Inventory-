export function sanitizeInput(value) {
  if (typeof value !== "string") return "";
  return value.trim().slice(0, 100);
}

export function isValidUsername(value) {
  return /^[a-zA-Z0-9_-]+$/.test(value);
}

export function isValidPassword(value) {
  return value.length >= 8;
}

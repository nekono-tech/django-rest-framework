export function useTextUtils() {
  const truncateText = (text, maxLength) => {
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
  }

  return {
    truncateText
  }
}

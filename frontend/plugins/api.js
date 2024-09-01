class ApiClient {
  constructor(baseURL) {
    this.client = $fetch.create({
      baseURL,
      onRequest({ request, options }) {
        console.log('onRequest ----------------------------------------------------');
        console.log('request:', request);
        console.log('options:', options);
      },
      onResponse({ response, options }) {
        console.log('onResponse ----------------------------------------------------');
        console.log('response:', response);
        console.log('options:', options);
      },
    });
  }

  async get(url, options = {}) {
    return this.request(url, { method: 'GET', ...options });
  }

  async post(url, body = {}, options = {}) {
    return this.request(url, { method: 'POST', body, ...options });
  }

  async put(url, body = {}, options = {}) {
    return this.request(url, { method: 'PUT', body, ...options });
  }

  async delete(url, options = {}) {
    return this.request(url, { method: 'DELETE', ...options });
  }

  async request(url, options) {
    try {
      return await this.client(url, options);
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  handleError(error) {
    console.error('API Error:', error);
  }
}

export default defineNuxtPlugin(() => {
  const baseURL = import.meta.server ? 'http://backend:8888/api/' : '/api/';
  const api = new ApiClient(baseURL);

  return {
    provide: {
      api,
    },
  };
});

export function serverAddr() {
  // return "localhost:8000";
  return "35.237.184.43:8000";
}

function apiVersion() {
  return "v1";
}

function baseUrl() {
  return `http://${serverAddr()}/fipe/${apiVersion()}/`;
}

export function makersUrl() {
  return `${baseUrl()}makers/?format=json`;
}

export function carsUrl(maker) {
  return `${baseUrl()}makers/${maker}/cars/?format=json`;
}

export function carsUrlUnique(maker) {
  return `${baseUrl()}makers/${maker}/cars/?format=json&unique=true`;
}

export function alertError(url) {
  const msg = `Looks like the server is down :/\n\nCouldn't fetch ${url}`;
  alert(msg);
}

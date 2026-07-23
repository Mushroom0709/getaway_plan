/**
 * 从 qinggan-travel 项目提取数据并输出为 JSON
 * 运行: node scripts/extract_data.js
 */
import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const QINGGAN = resolve(__dirname, '../../qinggan-travel/src/data');
const OUT = resolve(__dirname, '../scripts/data_export');

// 读取预编译的 JS 文件
function loadData(name) {
    const path = resolve(QINGGAN, name + '.ts');
    let code = readFileSync(path, 'utf-8');
    // Remove TypeScript type annotations: { key: type }
    code = code.replace(/: [A-Za-z<>[\],| "'/{}()]+(?=[,;)\n\r}])/g, '');
    // Remove import statements
    code = code.replace(/import .+ from .+/g, '');
    // Convert export const X: Type = to const X =
    code = code.replace(/export const (\w+): [^=]+ =/, 'const $1 =');
    // Convert Record<string, X> pattern
    code = code.replace(/: Record<string, [^>]+>/g, '');
    return code;
}

// Extract spots data
function extractSpots() {
    const code = loadData('spots');
    // Write to a temp file that can be evaluated
    const wrapped = code + '\nprocess.stdout.write(JSON.stringify(spots));';
    writeFileSync('/tmp/qinggan_spots.mjs', wrapped);
}

function extractHotels() {
    const code = loadData('hotels');
    const wrapped = code + '\nprocess.stdout.write(JSON.stringify(hotels));';
    writeFileSync('/tmp/qinggan_hotels.mjs', wrapped);
}

function extractFood() {
    const code = loadData('food');
    const wrapped = code + '\nprocess.stdout.write(JSON.stringify(restaurants));';
    writeFileSync('/tmp/qinggan_food.mjs', wrapped);
}

function extractItinerary() {
    const code = loadData('itinerary');
    const wrapped = code + '\nprocess.stdout.write(JSON.stringify(itinerary));';
    writeFileSync('/tmp/qinggan_itinerary.mjs', wrapped);
}

function extractBudget() {
    const code = loadData('budget');
    const wrapped = code + '\nprocess.stdout.write(JSON.stringify(budget));';
    writeFileSync('/tmp/qinggan_budget.mjs', wrapped);
}

function extractWeather() {
    const code = loadData('weather');
    const wrapped = code + '\nprocess.stdout.write(JSON.stringify(weather));';
    writeFileSync('/tmp/qinggan_weather.mjs', wrapped);
}

function extractRental() {
    const code = loadData('rental');
    const wrapped = code + '\nprocess.stdout.write(JSON.stringify(cars));';
    writeFileSync('/tmp/qinggan_rental.mjs', wrapped);
}

function extractPhotos() {
    const code = loadData('photos');
    const wrapped = code + '\nprocess.stdout.write(JSON.stringify(spotPhotos));';
    writeFileSync('/tmp/qinggan_photos.mjs', wrapped);
}

extractSpots();
extractHotels();
extractFood();
extractItinerary();
extractBudget();
extractWeather();
extractRental();
extractPhotos();
console.log('All data files extracted to /tmp/qinggan_*.mjs');

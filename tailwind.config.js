/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './party/templates/party/**/*.html',
        './party/static/party/js/**/*.js',
        './party/static/party/src/**/*.css',
        './**/*.py'
    ],
    safelist: [
        'bg-green-800'
    ],
    theme: {
        fontFamily: {
            sans: ["Roboto"] // setting the default font-family
        },
        extend: {
            fontFamily: {
                "roboto": ["Roboto", "sans-serif"], // making possible to use classes font-roboto and font-dancing-script
                "dancing-script": ["Dancing Script", "cursive"],
            },
            colors: {
                "custom-powder-light": "#eee2dc",
                "custom-powder": "#edc7b7",
                "custom-blue": "#123c69",
                "custom-blue-light": "#3a6aa4",
                "custom-red": "#ac3b61",
            },
        },
    },
    plugins: [],
}


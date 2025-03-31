// Optional sides like chips, drinks
export interface SideItem {
    name: "Chips" | "Chips & Guac" | "Chips & Queso" | "Drink";
    size?: "Small" | "Medium" | "Large"; // Optional for drinks
}
export interface Cart {
    items: OrderItem[];
    // notes?: string;  // Optional field for user preferences like "no napkins" or "extra hot sauce"
}

export interface OrderItem {
    id: string; // Unique identifier for managing edits/removals
    type: "Bowl" | "Burrito" | "Tacos" | "Salad" | "Quesadilla" | "Kid's Meal";
    protein: ProteinType;
    rice?: "White" | "Brown" | "None";
    beans?: "Black" | "Pinto" | "None";
    toppings?: Topping[];
    sides?: SideItem[];
    extras?: Extra[];
    quantity: number;
    // instructions?: string; // Free-text like "extra crispy tortilla" or "salsa on the side"
}

// Protein options
export type ProteinType =
  | "Chicken"
  | "Steak"
  | "Barbacoa"
  | "Carnitas"
  | "Sofritas"
  | "Veggie";

// Optional toppings
export type Topping =
  | "Lettuce"
  | "Fajita Veggies"
  | "Mild Salsa"
  | "Medium Salsa"
  | "Hot Salsa"
  | "Corn Salsa"
  | "Cheese"
  | "Sour Cream"
  | "Guacamole";

// Optional sides like chips, drinks
export interface SideItem {
  name: "Chips" | "Chips & Guac" | "Chips & Queso" | "Drink";
  size?: "Small" | "Medium" | "Large"; // Optional for drinks
}

// Extras (paid additions)
export type Extra = "Extra Cheese" | "Extra Guac" | "Double Meat";
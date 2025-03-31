export interface OrderItem {
  id: string;
  type: "Bowl" | "Burrito" | "Tacos" | "Salad" | "Quesadilla" | "Kid's Meal";
  protein: IngredientWithQuantity<ProteinType>;
  rice?: IngredientWithQuantity<RiceType>;
  beans?: IngredientWithQuantity<BeanType>;
  toppings?: IngredientWithQuantity<ToppingType>[];
  sides?: IngredientWithQuantity<SideType>[];
  drinks?: IngredientWithQuantity<DrinkType>[];
  quantity: number;
}

export type ProteinType =
  | "Chicken"
  | "Steak"
  | "Barbacoa"
  | "Carnitas"
  | "Sofritas"
  | "Veggie";

export type RiceType = "White" | "Brown" | "None";
export type BeanType = "Black" | "Pinto" | "None";
export type ToppingType =
  | "Lettuce"
  | "Fajita Veggies"
  | "Mild Salsa"
  | "Medium Salsa"
  | "Hot Salsa"
  | "Corn Salsa"
  | "Cheese"
  | "Sour Cream"
  | "Guacamole";

export type SideType = "Chips" | "Chips & Guac" | "Chips & Queso";
export type DrinkType = "Soda" | "Water" | "Lemonade";

// Generic reusable type
export interface IngredientWithQuantity<T = string> {
  name: T;
  quantity: number;
}

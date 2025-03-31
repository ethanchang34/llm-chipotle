import { OrderItem } from "./OrderItem";

export interface Cart {
    items: OrderItem[];
    // notes?: string;  // Optional field for user preferences like "no napkins" or "extra hot sauce"
}
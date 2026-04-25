/**
 * Types centraux du projet LAVERVOTREVEHICULE.FR
 * Définit les types partagés utilisés dans toute l'application.
 */

export type VehicleCategory = "camping-car" | "car" | "moto";

export type VehicleSize = "small" | "medium" | "large";

export type WashType = "hybrid" | "dry" | "exterior" | "interior";

export type PackageTier = "standard" | "premium";

export type PaymentType = "deposit" | "full";

export type BookingStatus = "pending" | "confirmed" | "completed" | "cancelled";

export type PaymentStatus = "pending" | "paid" | "failed" | "refunded";

export interface Money {
  amount: number;
  currency: "EUR";
}

export interface Address {
  street: string;
  city: string;
  postalCode: string;
  country: string;
  lat?: number;
  lng?: number;
}

export interface Customer {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  phone: string;
}

export interface Booking {
  id: string;
  customerId: string;
  category: VehicleCategory;
  vehicleSize?: VehicleSize;
  packageTier?: PackageTier;
  options: string[];
  totalPrice: Money;
  address: Address;
  distanceFromNiceKm: number;
  scheduledAt: Date;
  status: BookingStatus;
  paymentType: PaymentType;
  paymentStatus: PaymentStatus;
  stripePaymentIntentId?: string;
  invoiceUrl?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface WaterCounter {
  totalWashes: number;
  totalLitersSaved: number;
  updatedAt: Date;
}

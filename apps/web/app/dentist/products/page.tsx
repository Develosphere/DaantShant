import type { Metadata } from "next";
import { PortalSectionPage } from "@/components/portal/PortalSectionPage";

export const metadata: Metadata = {
  title: "Products — Dentist Portal",
};

export default function DentistProductsPage() {
  return (
    <PortalSectionPage
      role="dentist"
      title="Product catalog"
      description="Manage your dental product listings from /dentist/products. Coming soon."
    />
  );
}

import React from "react";
import { cn } from "@/lib/utils";

interface BadgeProps {
  children: React.ReactNode;
  className?: string;
  variant?: "default" | "success" | "warning" | "error";
}

const variantClasses = {
  default: "bg-gray-200 text-gray-800",
  success: "bg-green-200 text-green-800",
  warning: "bg-yellow-200 text-yellow-800",
  error: "bg-red-200 text-red-800",
};

export const Badge: React.FC<BadgeProps> = ({
  children,
  className = "",
  variant = "default",
}) => {
  return (
    <span
      className={cn(
        "inline-block rounded-full px-3 py-1 text-sm font-semibold",
        variantClasses[variant],
        className
      )}
    >
      {children}
    </span>
  );
};

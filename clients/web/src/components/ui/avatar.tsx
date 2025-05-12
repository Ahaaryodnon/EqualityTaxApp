import React from "react";
import { cn } from "@/lib/utils";

interface AvatarProps {
  src: string;
  alt: string;
  size?: "small" | "medium" | "large";
  className?: string;
}

const sizeClasses = {
  small: "w-8 h-8",
  medium: "w-12 h-12",
  large: "w-16 h-16",
};

export const Avatar: React.FC<AvatarProps> = ({
  src,
  alt,
  size = "medium",
  className = "",
}) => {
  return (
    <img
      src={src}
      alt={alt}
      className={cn(
        "rounded-full object-cover",
        sizeClasses[size],
        className
      )}
    />
  );
};

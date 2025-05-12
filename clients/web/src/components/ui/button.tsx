import { cn } from "@/lib/utils";
import { ButtonHTMLAttributes, forwardRef } from "react";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: "primary" | "secondary";
};

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
    ({ variant = "primary", className, ...props }, ref) => {
        const baseStyles = "px-4 py-2 font-medium rounded focus:outline-none focus:ring";
        const variantStyles =
            variant === "primary"
                ? "bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-300"
                : "bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-400";

        return (
            <button
                ref={ref}
                className={cn(baseStyles, variantStyles, className)}
                {...props}
            />
        );
    }
);

Button.displayName = "Button";

export { Button };

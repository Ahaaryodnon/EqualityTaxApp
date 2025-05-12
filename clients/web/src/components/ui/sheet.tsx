import { cn } from "@/lib/utils";
import { forwardRef, ReactNode } from "react";

type SheetProps = {
  children: ReactNode;
  isOpen: boolean;
  onClose: () => void;
};

const Sheet = forwardRef<HTMLDivElement, SheetProps>(
  ({ children, isOpen, onClose }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "fixed inset-0 z-50 flex items-center justify-center transition-opacity",
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        )}
        onClick={onClose}
      >
        <div
          className="bg-white rounded shadow-lg p-4"
          onClick={(e) => e.stopPropagation()}
        >
          {children}
        </div>
      </div>
    );
  }
);

Sheet.displayName = "Sheet";

export { Sheet };

import { type ColorPaletteCustom } from "@excalidraw/common";
import type { Theme } from "@excalidraw/element/types";
interface ShadeListProps {
    theme: Theme;
    color: string | null;
    onChange: (color: string) => void;
    palette: ColorPaletteCustom;
    showHotKey?: boolean;
}
export declare const ShadeList: ({ theme, color, onChange, palette, showHotKey, }: ShadeListProps) => import("react/jsx-runtime").JSX.Element;
export {};

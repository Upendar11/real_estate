import type { ElementsMap, NonDeletedExcalidrawElement } from "@excalidraw/element/types";
import type { Scene } from "@excalidraw/element";
import type { AppState } from "../../types";
interface PositionProps {
    property: "x" | "y";
    element: NonDeletedExcalidrawElement;
    elementsMap: ElementsMap;
    scene: Scene;
    appState: AppState;
}
declare const Position: ({ property, element, scene, appState }: PositionProps) => import("react/jsx-runtime").JSX.Element;
export default Position;

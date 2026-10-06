import type { ElementsMap, NonDeletedExcalidrawElement } from "@excalidraw/element/types";
import type { Scene } from "@excalidraw/element";
import type { AtomicUnit } from "./utils";
import type { AppState } from "../../types";
interface MultiPositionProps {
    property: "x" | "y";
    elements: readonly NonDeletedExcalidrawElement[];
    elementsMap: ElementsMap;
    atomicUnits: AtomicUnit[];
    scene: Scene;
    appState: AppState;
}
declare const MultiPosition: ({ property, elements, elementsMap, atomicUnits, scene, appState, }: MultiPositionProps) => import("react/jsx-runtime").JSX.Element;
export default MultiPosition;

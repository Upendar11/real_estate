import type { AppClassProperties, AppState } from "../types";
export declare const distributeHorizontally: {
    name: "distributeHorizontally";
    label: string;
    trackEvent: {
        category: "element";
    };
    perform: (elements: readonly import("@excalidraw/element/types").OrderedExcalidrawElement[], appState: Readonly<AppState>, _: unknown, app: AppClassProperties) => {
        appState: Readonly<AppState>;
        elements: (import("@excalidraw/element/types").ExcalidrawLinearElement | import("@excalidraw/element/types").ExcalidrawSelectionElement | import("@excalidraw/element/types").ExcalidrawRectangleElement | import("@excalidraw/element/types").ExcalidrawStickyNoteElement | import("@excalidraw/element/types").ExcalidrawDiamondElement | import("@excalidraw/element/types").ExcalidrawEllipseElement | import("@excalidraw/element/types").ExcalidrawEmbeddableElement | import("@excalidraw/element/types").ExcalidrawIframeElement | import("@excalidraw/element/types").ExcalidrawImageElement | import("@excalidraw/element/types").ExcalidrawFrameElement | import("@excalidraw/element/types").ExcalidrawMagicFrameElement | import("@excalidraw/element/types").ExcalidrawTextElement | import("@excalidraw/element/types").ExcalidrawFreeDrawElement)[];
        captureUpdate: "IMMEDIATELY";
    };
    keyTest: (event: KeyboardEvent | import("react").KeyboardEvent<Element>) => boolean;
    PanelComponent: ({ elements, appState, updateData, app }: import("./types").PanelComponentProps) => import("react/jsx-runtime").JSX.Element;
} & {
    keyTest?: ((event: KeyboardEvent | import("react").KeyboardEvent<Element>) => boolean) | undefined;
};
export declare const distributeVertically: {
    name: "distributeVertically";
    label: string;
    trackEvent: {
        category: "element";
    };
    perform: (elements: readonly import("@excalidraw/element/types").OrderedExcalidrawElement[], appState: Readonly<AppState>, _: unknown, app: AppClassProperties) => {
        appState: Readonly<AppState>;
        elements: (import("@excalidraw/element/types").ExcalidrawLinearElement | import("@excalidraw/element/types").ExcalidrawSelectionElement | import("@excalidraw/element/types").ExcalidrawRectangleElement | import("@excalidraw/element/types").ExcalidrawStickyNoteElement | import("@excalidraw/element/types").ExcalidrawDiamondElement | import("@excalidraw/element/types").ExcalidrawEllipseElement | import("@excalidraw/element/types").ExcalidrawEmbeddableElement | import("@excalidraw/element/types").ExcalidrawIframeElement | import("@excalidraw/element/types").ExcalidrawImageElement | import("@excalidraw/element/types").ExcalidrawFrameElement | import("@excalidraw/element/types").ExcalidrawMagicFrameElement | import("@excalidraw/element/types").ExcalidrawTextElement | import("@excalidraw/element/types").ExcalidrawFreeDrawElement)[];
        captureUpdate: "IMMEDIATELY";
    };
    keyTest: (event: KeyboardEvent | import("react").KeyboardEvent<Element>) => boolean;
    PanelComponent: ({ elements, appState, updateData, app }: import("./types").PanelComponentProps) => import("react/jsx-runtime").JSX.Element;
} & {
    keyTest?: ((event: KeyboardEvent | import("react").KeyboardEvent<Element>) => boolean) | undefined;
};

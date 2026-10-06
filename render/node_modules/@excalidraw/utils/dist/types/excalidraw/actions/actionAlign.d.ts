import type { ExcalidrawElement } from "@excalidraw/element/types";
import type { AppClassProperties, AppState, UIAppState } from "../types";
export declare const alignActionsPredicate: (appState: UIAppState, app: AppClassProperties) => boolean;
export declare const actionAlignTop: {
    name: "alignTop";
    label: string;
    icon: import("react/jsx-runtime").JSX.Element;
    trackEvent: {
        category: "element";
    };
    predicate: (elements: readonly ExcalidrawElement[], appState: AppState, appProps: import("../types").ExcalidrawProps, app: AppClassProperties) => boolean;
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
export declare const actionAlignBottom: {
    name: "alignBottom";
    label: string;
    icon: import("react/jsx-runtime").JSX.Element;
    trackEvent: {
        category: "element";
    };
    predicate: (elements: readonly ExcalidrawElement[], appState: AppState, appProps: import("../types").ExcalidrawProps, app: AppClassProperties) => boolean;
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
export declare const actionAlignLeft: {
    name: "alignLeft";
    label: string;
    icon: import("react/jsx-runtime").JSX.Element;
    trackEvent: {
        category: "element";
    };
    predicate: (elements: readonly ExcalidrawElement[], appState: AppState, appProps: import("../types").ExcalidrawProps, app: AppClassProperties) => boolean;
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
export declare const actionAlignRight: {
    name: "alignRight";
    label: string;
    icon: import("react/jsx-runtime").JSX.Element;
    trackEvent: {
        category: "element";
    };
    predicate: (elements: readonly ExcalidrawElement[], appState: AppState, appProps: import("../types").ExcalidrawProps, app: AppClassProperties) => boolean;
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
export declare const actionAlignVerticallyCentered: {
    name: "alignVerticallyCentered";
    label: string;
    icon: import("react/jsx-runtime").JSX.Element;
    trackEvent: {
        category: "element";
    };
    predicate: (elements: readonly ExcalidrawElement[], appState: AppState, appProps: import("../types").ExcalidrawProps, app: AppClassProperties) => boolean;
    perform: (elements: readonly import("@excalidraw/element/types").OrderedExcalidrawElement[], appState: Readonly<AppState>, _: unknown, app: AppClassProperties) => {
        appState: Readonly<AppState>;
        elements: (import("@excalidraw/element/types").ExcalidrawLinearElement | import("@excalidraw/element/types").ExcalidrawSelectionElement | import("@excalidraw/element/types").ExcalidrawRectangleElement | import("@excalidraw/element/types").ExcalidrawStickyNoteElement | import("@excalidraw/element/types").ExcalidrawDiamondElement | import("@excalidraw/element/types").ExcalidrawEllipseElement | import("@excalidraw/element/types").ExcalidrawEmbeddableElement | import("@excalidraw/element/types").ExcalidrawIframeElement | import("@excalidraw/element/types").ExcalidrawImageElement | import("@excalidraw/element/types").ExcalidrawFrameElement | import("@excalidraw/element/types").ExcalidrawMagicFrameElement | import("@excalidraw/element/types").ExcalidrawTextElement | import("@excalidraw/element/types").ExcalidrawFreeDrawElement)[];
        captureUpdate: "IMMEDIATELY";
    };
    PanelComponent: ({ elements, appState, updateData, app }: import("./types").PanelComponentProps) => import("react/jsx-runtime").JSX.Element;
} & {
    keyTest?: undefined;
};
export declare const actionAlignHorizontallyCentered: {
    name: "alignHorizontallyCentered";
    label: string;
    icon: import("react/jsx-runtime").JSX.Element;
    trackEvent: {
        category: "element";
    };
    predicate: (elements: readonly ExcalidrawElement[], appState: AppState, appProps: import("../types").ExcalidrawProps, app: AppClassProperties) => boolean;
    perform: (elements: readonly import("@excalidraw/element/types").OrderedExcalidrawElement[], appState: Readonly<AppState>, _: unknown, app: AppClassProperties) => {
        appState: Readonly<AppState>;
        elements: (import("@excalidraw/element/types").ExcalidrawLinearElement | import("@excalidraw/element/types").ExcalidrawSelectionElement | import("@excalidraw/element/types").ExcalidrawRectangleElement | import("@excalidraw/element/types").ExcalidrawStickyNoteElement | import("@excalidraw/element/types").ExcalidrawDiamondElement | import("@excalidraw/element/types").ExcalidrawEllipseElement | import("@excalidraw/element/types").ExcalidrawEmbeddableElement | import("@excalidraw/element/types").ExcalidrawIframeElement | import("@excalidraw/element/types").ExcalidrawImageElement | import("@excalidraw/element/types").ExcalidrawFrameElement | import("@excalidraw/element/types").ExcalidrawMagicFrameElement | import("@excalidraw/element/types").ExcalidrawTextElement | import("@excalidraw/element/types").ExcalidrawFreeDrawElement)[];
        captureUpdate: "IMMEDIATELY";
    };
    PanelComponent: ({ elements, appState, updateData, app }: import("./types").PanelComponentProps) => import("react/jsx-runtime").JSX.Element;
} & {
    keyTest?: undefined;
};

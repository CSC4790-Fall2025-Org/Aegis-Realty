import { useEffect } from "react";

export const useScrollToTop = () => {
    useEffect(() => {
        window.scroll(0, 0);
    }, []);
};
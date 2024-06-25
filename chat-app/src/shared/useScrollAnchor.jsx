import { useEffect, useRef, useState } from "react";

export const useScrollAnchor = () => {
  const visibilityRef = useRef(null);
  const scrollRef = useRef(null);
  const messagesRef = useRef(null);

  const [isAtBottom, setIsAtBottom] = useState(true);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (messagesRef.current) {
      if (!isVisible) {
        console.log("scroll up");
        messagesRef.current.scrollIntoView({
          block: "end",
          behavior: "smooth",
        });
      }
    }
  }, [isVisible,isAtBottom]);

  useEffect(() => {
    const { current } = scrollRef
    
    if (current) {
      console.log(current)
      const handleScroll = (event) => {
        const target = event.target
        const offset = 25
        const isAtBottom =
          target.scrollTop + target.clientHeight >= target.scrollHeight - offset

        console.log("isBottom", isAtBottom)
        setIsAtBottom(isAtBottom)
      }

      current.addEventListener('scroll', handleScroll, {
        passive: true
      })

      return () => {
        current.removeEventListener('scroll', handleScroll)
      }
    }
  }, [])


  useEffect(() => {
    if (visibilityRef.current) {
      let observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              setIsVisible(true);
              console.log("intersecting", true);
            } else {
              setIsVisible(false);
              console.log("intersecting", false);
              messagesRef.current.scrollIntoView({
                block: "end",
                behavior: "smooth",
              });      
            }
          });
        },
        {
          rootMargin: "0px 0px -200px 0px",
        }
      );

      observer.observe(visibilityRef.current);

      return () => {
        observer.disconnect();
      };
    }
  });

  return { visibilityRef, scrollRef, messagesRef, isVisible };
};

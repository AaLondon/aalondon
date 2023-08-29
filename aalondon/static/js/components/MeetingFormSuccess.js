
import React, { useEffect, useState, useRef } from "react";


export default function MeetingFormSuccess(props) {
  const [isLoading, setIsLoading] = useState(true);
  const resultsRef = useRef(null)
  useEffect(
    () => {
      if (resultsRef.current) {
        window.scrollTo({
          behavior: "smooth",
          top: 0
        });
      }
    },
    [isLoading]
  );

  return (
    <React.Fragment>
      <div ref={resultsRef}>
        Thank you for submitting your meeting details. You will receive an email with a confirmation link, Once confirmed one of our team members will review your submission and will publish your changes within 48 hours. If you need any more assistance or have questions please email ecomm.ln@aamail.org.
        </div>
    </React.Fragment>
  );
}

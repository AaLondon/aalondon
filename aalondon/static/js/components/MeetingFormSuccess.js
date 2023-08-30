
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
      <div ref={resultsRef} className="text-center">
        <p>Thank you for submitting your meeting details. You will receive an email with a confirmation link. If you need any more assistance or have questions please email ecomm.ln@aamail.org.</p>
        </div>
    </React.Fragment>
  );
}

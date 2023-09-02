
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
        <p>Thank you for submitting your details. You will receive an email with a confirmation links shortly - please check your spam or junk folders if not received in your inbox. PLEASE NOTE: you will need to click on the link to verify your email address before we can publish your updates. If you need any more assistance or have questions, please email info@aa-london.com</p>
        </div>
    </React.Fragment>
  );
}

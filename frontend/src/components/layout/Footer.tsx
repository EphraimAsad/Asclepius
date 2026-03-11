export function Footer() {
  return (
    <footer className="bg-gray-100 border-t border-gray-200 py-6">
      <div className="container mx-auto px-4">
        <div className="text-center text-sm text-gray-500">
          <p className="mb-2">
            <strong>Asclepius</strong> - Educational Health Information Tool
          </p>
          <p>
            This tool is for educational purposes only. It is not a substitute
            for professional medical advice, diagnosis, or treatment.
          </p>
          <p className="mt-2 text-red-600 font-medium">
            If you are experiencing a medical emergency, call 911 immediately.
          </p>
        </div>
      </div>
    </footer>
  );
}

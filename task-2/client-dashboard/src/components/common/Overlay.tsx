import { DotLottieReact } from '@lottiefiles/dotlottie-react';

const Overlay = () => {
    return (
        <div className="fixed inset-0 bg-gray-800 bg-opacity-75 z-50 flex flex-col justify-center items-center">
            <DotLottieReact
                src="https://lottie.host/81fdf35e-2e70-4b34-8dc1-d3daaf062c41/4b5vf74xhp.lottie"
                loop
                autoplay
            />
            {/* Spacer to push the text to the bottom */}
            <div className="flex-grow" />
            <div className="mb-8">
                <h1 className="text-white text-2xl font-semibold">Loading Turbine Assets, Please Wait...</h1>
            </div>
        </div>
    );
}

export default Overlay;
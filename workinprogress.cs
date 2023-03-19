using System;
using System.Threading;

namespace KeyPressChallenge
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Press the following keys within 3 seconds each time to win!");
            var cts = new CancellationTokenSource();
            ThreadPool.QueueUserWorkItem(s => CheckKeyPress(cts.Token));

            bool success = false;
            try
            {
                if (Console.ReadKey(true).Key == ConsoleKey.UpArrow)
                {
                    success = true;
                }
            }
            catch (InvalidOperationException)
            {
                // Ignore exceptions thrown by Console.ReadKey() when the operation is cancelled.
            }

            cts.Cancel();

            if (success)
            {
                Console.WriteLine("Success!");
            }
            else
            {
                Console.WriteLine("Failure!");
            }

            Console.WriteLine("Press any key to exit.");
            Console.ReadKey(true);
        }

        static void CheckKeyPress(CancellationToken cancellationToken)
        {
            try
            {
                if (!cancellationToken.WaitHandle.WaitOne(3000))
                {
                    Console.WriteLine("Time's up!");
                    Console.WriteLine("Failure!");
                    Environment.Exit(0);
                }
            }
            catch (OperationCanceledException)
            {
                // Ignore exceptions thrown when the operation is cancelled.
            }
        }
    }
}
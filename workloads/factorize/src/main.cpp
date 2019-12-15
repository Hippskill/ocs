#include <atomic>
#include <fstream>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>
#include <vector>

using namespace std::chrono_literals;

std::vector<int64_t> factorize(int64_t x) {
  std::vector<int64_t> result;
  for (int64_t i = 2; i * i <= x; ++i) {
    while (x % i == 0) {
      result.push_back(i);
      x /= i;
    }
  }
  if (x > 1) {
    result.push_back(x);
  }
  return result;
}

template<typename T>
class OneToOneQueue {
public:
  void push(T&& x) {
    std::lock_guard lock(mutex_);
    queue_.push(std::move(x));
  }

  bool pop(T* x) {
    std::lock_guard lock(mutex_);
    if (queue_.empty()) {
      return false;
    }
    *x = std::move(queue_.front());
    queue_.pop();
    return true;
  }

  size_t size() const {
    std::lock_guard lock(mutex_);
    return queue_.size();
  }

private:
  std::queue<T> queue_;
  mutable std::mutex mutex_;
};

int main(int, char** argv) {
  const std::string input_file = argv[1];
  const std::string output_file = argv[2];
  const size_t max_threads = std::thread::hardware_concurrency();
  std::atomic<bool> stopped = false;
  OneToOneQueue<int64_t> to_factorize;
  OneToOneQueue<std::pair<int64_t, std::vector<int64_t>>> result;

  std::vector<std::thread> threads;
  for (size_t i = 0; i < max_threads; ++i) {
    threads.push_back(std::thread(
        [&] {
          while (!stopped) {
            int64_t x;
            if (to_factorize.pop(&x)) {
              std::cout << "thread: " << std::this_thread::get_id() << " start factorize: " << x << std::endl;
              result.push({x, factorize(x)});
              std::cout << "thread: " << std::this_thread::get_id() << " finish factorize: " << x << std::endl;
            }
          } 
        }
    ));
  }

  std::ifstream input;
  input.open(input_file);

  int64_t x;
  while (input >> x) {
    to_factorize.push(std::move(x));
  }

  while (true) {
    auto current_queue_size = to_factorize.size();
    std::cout << "remain size: " << current_queue_size << std::endl;

    if (current_queue_size == 0) {
      break;
    }
    std::this_thread::sleep_for(2s);
  }

  stopped = true;

  for (auto&& t : threads) {
    t.join();
  }

  std::ofstream output;
  output.open(output_file);
  std::pair<int64_t, std::vector<int64_t>> factorization;
  while (result.pop(&factorization)) {
    output << factorization.first << " :  ";
    for (auto x : factorization.second) {
      output << x << " ";
    }
    output << "\n";
  }
}

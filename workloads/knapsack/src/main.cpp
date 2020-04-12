#include <algorithm>
#include <cassert>
#include <chrono>
#include <cmath>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <memory>
#include <numeric>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std::chrono;

struct Item {
    int cost;
    int weight;
    int id;

    Item() = default;
    Item(int cost, int weight, int id) : cost(cost), weight(weight), id(id) {
    }
};

struct Input {
    int n{0};
    int W{0};
    std::vector<Item> items;
};

struct Output {
    int P{0};
    std::vector<Item> items;

    void Add(Item item) {
        P += item.cost;
        items.emplace_back(std::move(item));
    }

    void PopBack() {
        P -= items.back().cost;
        items.pop_back();
    }
};

class ISolution {
public:
    virtual ~ISolution() = default;

    virtual Output Solve(const Input& input) = 0;
};

template <class Solution>
Output RunSolution(const Input& input) {
    Solution solution;
    return solution.Solve(input);
}

class SolutionFactory {
public:
    template <class Solution,
              class = std::enable_if_t<std::is_base_of<ISolution, Solution>::value>>
    void RegisterSolution(const std::string name) {
        creators_.emplace(name, [] { return std::make_unique<Solution>(); });
    }

    std::vector<std::pair<std::string, std::unique_ptr<ISolution>>> AllSolutions() const {
        std::vector<std::pair<std::string, std::unique_ptr<ISolution>>> solutions;

        solutions.reserve(creators_.size());
        for (const auto& kv : creators_) {
            const auto& name = kv.first;
            const auto& creator = kv.second;
            solutions.emplace_back(name, creator());
        }

        return solutions;
    }

private:
    std::unordered_map<std::string,
                       std::function<std::unique_ptr<ISolution>()>> creators_;
};

SolutionFactory* GetSolutionFactory() {
    static SolutionFactory factory;
    return &factory;
}

auto AllSolutions() {
    return GetSolutionFactory()->AllSolutions();
}

#define REGISTER_SOLUTION(solution)                                 \
static auto dummy_##solution = [] {                                 \
    GetSolutionFactory()->RegisterSolution<solution>(#solution);    \
    return 0;                                                       \
}();                                                                \

#define LOG(message)                                                \
do {                                                                \
    std::cerr << "[" << __func__ << "] " << message << std::endl;   \
} while (false);                                                    \

class GreedySolution : public ISolution {
public:
    Output Solve(const Input& input) {
        Output output;

        auto items = input.items;
        std::sort(items.begin(), items.end(), [](const auto& lhs, const auto& rhs) {
            auto profit = [](const auto item) -> double {
                return static_cast<double>(item.cost) / item.weight;
            };
            return profit(lhs) > profit(rhs);
        });

        int remain_W = input.W;
        for (const auto& item : items) {
            if (item.weight <= remain_W) {
                remain_W -= item.weight;
                output.Add(item);
            }
        }

        return output;
    }
};

REGISTER_SOLUTION(GreedySolution);

enum class EDpType {
    COST = 0,
    WEIGHT = 1
};

template <EDpType Type>
class DPByTypeSolution : public ISolution {
public:
    DPByTypeSolution() {
        if constexpr (Type == EDpType::COST) {
            default_value_ = std::numeric_limits<int>::max();
        } else if constexpr (Type == EDpType::WEIGHT) {
            default_value_ = -1;
        }
    }

    Output Solve(const Input& input) {
        Output output;

        const auto dp = CalcDP(input);

        std::pair<int, int> result = {0, 0};
        for (int i = 0; i < dp.size(); ++i) {
            if constexpr (Type == EDpType::COST) {
                if (dp[i] != std::numeric_limits<int>::max()) {
                    result = {i, dp[i]};
                }
            } else if constexpr (Type == EDpType::WEIGHT) {
                if (dp[i] > result.first) {
                    result = {dp[i], i};
                }
            }
        }

        RestoreAnswer(input, result.first, result.second, output);

        return output;
    }

private:
    std::vector<int> CalcDP(const Input& input) {
        const auto& dp_items = input.items;
        const size_t n = dp_items.size();

        int bound = 0;
        if constexpr (Type == EDpType::COST) {
            bound = 2 * RunSolution<GreedySolution>(input).P;
        } else if constexpr (Type == EDpType::WEIGHT) {
            bound = input.W;
        }

        static constexpr size_t kBufferSize = 2;
        std::vector<std::vector<int>> dp(kBufferSize, std::vector<int>(bound + 1, default_value_));
        dp[0][0] = 0;

        for (int i = 0; i < n; ++i) {
            const int cur = i % kBufferSize;
            const int next = (i + 1) % kBufferSize;

            std::fill(dp[next].begin(), dp[next].end(), default_value_);
            for (int j = 0; j <= bound; ++j) {
                if (dp[cur][j] == default_value_) {
                    continue;
                }
                if constexpr (Type == EDpType::COST) {
                    dp[next][j] = std::min(dp[next][j], dp[cur][j]);
                    const int new_cost = j + dp_items[i].cost;
                    const int new_weight = dp[cur][j] + dp_items[i].weight;
                    if (new_cost > bound) {
                        continue;
                    }
                    if (new_weight > input.W) {
                        continue;
                    }
                    dp[next][new_cost] = std::min(dp[next][new_cost], new_weight);
                } else if constexpr (Type == EDpType::WEIGHT) {
                    dp[next][j] = std::max(dp[next][j], dp[cur][j]);

                    const int new_cost = dp[cur][j] + dp_items[i].cost;
                    const int new_weight = j + dp_items[i].weight;

                    if (new_weight > input.W) {
                        continue;
                    }

                    dp[next][new_weight] = std::max(dp[next][new_weight], new_cost);
                }
            }
        }

        return dp[n % kBufferSize];
    }

    void RestoreAnswer(const Input& input, int opt_cost, int opt_weight, Output& output) {
        if (opt_weight == 0 || opt_cost == 0) {
            return;
        }
        if (input.n == 0) {
            return;
        }
        if (input.n == 1) {
            assert(input.items.front().cost == opt_cost);
            assert(input.items.front().weight <= opt_weight);
            output.Add(input.items.front());
            return;
        }
        Input left;
        for (int i = 0; i < input.n / 2; ++i) {
            left.items.push_back(input.items[i]);
            ++left.n;
        }
        left.W = opt_weight;

        Input right;
        for (int i = input.n / 2; i < input.n; ++i) {
            right.items.push_back(input.items[i]);
            ++right.n;
        }
        right.W = opt_weight;

        const auto left_dp = CalcDP(left);
        const auto right_dp = CalcDP(right);

        for (int i = 0; i < left_dp.size(); ++i) {
            if (left_dp[i] == default_value_) {
                continue;
            }
            if constexpr (Type == EDpType::COST) {
                if (opt_cost - i < right_dp.size()) {
                    if (right_dp[opt_cost - i] == default_value_) {
                        continue;
                    }
                    if (right_dp[opt_cost - i] + left_dp[i] <= opt_weight) {
                        RestoreAnswer(left, i, left_dp[i], output);
                        RestoreAnswer(right, opt_cost - i, right_dp[opt_cost - i], output);
                        return;
                    }
                }
            } else if constexpr (Type == EDpType::WEIGHT) {
                if (opt_weight - i < right_dp.size()) {
                    if (right_dp[opt_weight - i] == default_value_) {
                        continue;
                    }
                    if (right_dp[opt_weight - i] + left_dp[i] == opt_cost) {
                        RestoreAnswer(left, left_dp[i], i, output);
                        RestoreAnswer(right, right_dp[opt_weight - i], opt_weight - i, output);
                        return;
                    }
                }
            }
        }

        assert(false);
    }

private:
    int default_value_{-1};
};

using DPByCostSolution = DPByTypeSolution<EDpType::COST>;
using DPByWeightSolution = DPByTypeSolution<EDpType::WEIGHT>;

class DPSolution : public ISolution {
public:
    Output Solve(const Input& input) {
        const int max_cost = 2 * RunSolution<GreedySolution>(input).P;
        if (max_cost > input.W) {
            return RunSolution<DPByWeightSolution>(input);
        } else {
            return RunSolution<DPByCostSolution>(input);
        }
    };
};

class BranchAndBoundSolution : public ISolution {
public:
    Output Solve(const Input& input_base) {
        Input input = input_base;
        std::sort(input.items.begin(), input.items.end(), [](const auto& lhs, const auto& rhs) {
            auto profit = [](const auto item) -> double {
                return static_cast<double>(item.cost) / item.weight;
            };
            return profit(lhs) > profit(rhs);
        });

        std::vector<int64_t> ps_weight(input.items.size() + 1);
        std::vector<int64_t> ps_cost(input.items.size() + 1);
        for (size_t i = 0; i < input.items.size(); ++i) {
            ps_weight[i + 1] = ps_weight[i] + input.items[i].weight;
            ps_cost[i + 1] = ps_cost[i] + input.items[i].cost;
        }

        Output output = RunSolution<GreedySolution>(input);

        Output dummy;
        Go(input, ps_weight, ps_cost, /* prefix */ 0, input.W, dummy, output);

        return output;
    }

private:
    void Go(
        const Input& input,
        const std::vector<int64_t>& ps_weight,
        const std::vector<int64_t>& ps_cost,
        int prefix,
        int rem_W,
        Output& output,
        Output& best_output)
    {
        if (iter++ > kIterLimit) {
            return;
        }
        if (output.P > best_output.P) {
            best_output = output;
        }
        if (prefix == input.n) {
            return;
        }
        if (Bound(input, ps_weight, ps_cost, prefix, rem_W) + output.P <= best_output.P) {
            return;
        }
        auto item = input.items[prefix];
        if (item.weight <= rem_W) {
            assert(item.id != 0);
            output.Add(item);
            Go(input, ps_weight, ps_cost, prefix + 1, rem_W - item.weight, output, best_output);
            assert(item.id == output.items.back().id);
            output.PopBack();
        }
        Go(input, ps_weight, ps_cost, prefix + 1, rem_W, output, best_output);
    }

    int Bound(
        const Input& input,
        const std::vector<int64_t>& ps_weight,
        const std::vector<int64_t>& ps_cost,
        int prefix,
        int rem_W)
    {
        int l = prefix - 1;
        int r = input.n;
        while (r - l > 1) {
            int mid = (r + l) / 2;
            if (ps_weight[mid] - ps_weight[prefix - 1] <= rem_W) {
                l = mid;
            } else {
                r = mid;
            }
        }

        int P = ps_cost[l] - ps_cost[prefix - 1];
        rem_W -= ps_weight[l] - ps_weight[prefix - 1];
        P += std::ceil(input.items[r].cost * (static_cast<double>(rem_W) / input.items[r].weight));
        return P;
    }

private:
    size_t iter{0};
    static constexpr size_t kIterLimit = 50000000;
};

template <int Threshold, class MiddleSolution>
class ThresholdSolution : public ISolution {
public:
    Output Solve(const Input& input_base) {
        Output output;

        Input input = input_base;

        auto items = input.items;
        std::sort(items.begin(), items.end(), [](const auto& lhs, const auto& rhs) {
            auto profit = [](const auto item) -> double {
                return static_cast<double>(item.cost) / item.weight;
            };
            return profit(lhs) > profit(rhs);
        });


        const int border = FindBorder(items, input.W);
        for (int i = 0; i < border - Threshold; ++i) {
            input.W -= items[i].weight;
            output.Add(items[i]);
        }

        Input middle_input;
        middle_input.W = input.W;
        middle_input.items.assign(
            items.begin() + std::max<int>(0, border - Threshold),
            items.begin() + std::min<int>(items.size(), border + Threshold)
        );
        middle_input.n = middle_input.items.size();

        const Output middle_output = RunSolution<MiddleSolution>(middle_input);
        for (const auto& item : middle_output.items) {
            input.W -= item.weight;
            output.Add(item);
        }

        for (int i = border + Threshold; i < items.size(); ++i) {
            if (items[i].weight <= input.W) {
                input.W -= items[i].weight;
                output.Add(items[i]);
            }
        }

        return output;
    }

private:
    int FindBorder(const std::vector<Item>& items, int max_W) {
        int border = 0;
        while (border < items.size() && items[border].weight <= max_W) {
            max_W -= items[border].weight;
            ++border;
        }
        return border;
    }
};

template <size_t Threshold>
using DPThresholdSolution = ThresholdSolution<Threshold, DPSolution>;

#define REGISTER_DP_THRESHOLD_SOLUTION(Threshold)                            \
using DPThresholdSolution_ ## Threshold  = DPThresholdSolution<Threshold>;   \
REGISTER_SOLUTION(DPThresholdSolution_ ## Threshold);                        \

REGISTER_DP_THRESHOLD_SOLUTION(5);
REGISTER_DP_THRESHOLD_SOLUTION(10);
REGISTER_DP_THRESHOLD_SOLUTION(20);
REGISTER_DP_THRESHOLD_SOLUTION(30);
REGISTER_DP_THRESHOLD_SOLUTION(40);
REGISTER_DP_THRESHOLD_SOLUTION(50);
REGISTER_DP_THRESHOLD_SOLUTION(60);
REGISTER_DP_THRESHOLD_SOLUTION(70);
REGISTER_DP_THRESHOLD_SOLUTION(80);
REGISTER_DP_THRESHOLD_SOLUTION(90);
REGISTER_DP_THRESHOLD_SOLUTION(100);
REGISTER_DP_THRESHOLD_SOLUTION(200);
REGISTER_DP_THRESHOLD_SOLUTION(300);
REGISTER_DP_THRESHOLD_SOLUTION(360);
REGISTER_DP_THRESHOLD_SOLUTION(500);
REGISTER_DP_THRESHOLD_SOLUTION(600);
REGISTER_DP_THRESHOLD_SOLUTION(700);
REGISTER_DP_THRESHOLD_SOLUTION(800);
REGISTER_DP_THRESHOLD_SOLUTION(900);
REGISTER_DP_THRESHOLD_SOLUTION(1000);
REGISTER_DP_THRESHOLD_SOLUTION(5000);
REGISTER_DP_THRESHOLD_SOLUTION(10000);
REGISTER_DP_THRESHOLD_SOLUTION(20000);

template <size_t Threshold>
using BranchAndBoundThresholdSolution = ThresholdSolution<Threshold, BranchAndBoundSolution>;

#define REGISTER_BRANCH_AND_BOUND_THRESHOLD_SOLUTION(Threshold)                                      \
using BranchAndBoundThresholdSolution_ ## Threshold  = BranchAndBoundThresholdSolution<Threshold>;   \
REGISTER_SOLUTION(BranchAndBoundThresholdSolution_ ## Threshold);                                    \

/*
REGISTER_BRANCH_AND_BOUND_THRESHOLD_SOLUTION(200);
REGISTER_BRANCH_AND_BOUND_THRESHOLD_SOLUTION(300);
REGISTER_BRANCH_AND_BOUND_THRESHOLD_SOLUTION(400);
REGISTER_BRANCH_AND_BOUND_THRESHOLD_SOLUTION(500);
REGISTER_BRANCH_AND_BOUND_THRESHOLD_SOLUTION(600);
REGISTER_BRANCH_AND_BOUND_THRESHOLD_SOLUTION(700);
REGISTER_BRANCH_AND_BOUND_THRESHOLD_SOLUTION(800);
REGISTER_BRANCH_AND_BOUND_THRESHOLD_SOLUTION(900);
REGISTER_BRANCH_AND_BOUND_THRESHOLD_SOLUTION(1000);
REGISTER_BRANCH_AND_BOUND_THRESHOLD_SOLUTION(1100);
REGISTER_BRANCH_AND_BOUND_THRESHOLD_SOLUTION(1200);
REGISTER_BRANCH_AND_BOUND_THRESHOLD_SOLUTION(1300);
*/

template <int K>
class ScaledDPSolution : public ISolution {
public:
    Output Solve(const Input& input_base) {
        Input input = input_base;

        Output output;

        for (auto& item : input.items) {
            item.cost = std::floor(static_cast<double>(item.cost) / K);
        }

        const Output scaled_output = RunSolution<DPByCostSolution>(input);
        for (const auto& item : scaled_output.items) {
            assert(input_base.items[item.id - 1].id == item.id);
            output.Add(input_base.items[item.id - 1]);
        }

        return output;
    }

private:
    int FindMaxCost(const Input& input) {
        int max_cost = 0;
        for (const auto& item : input.items) {
            max_cost = std::max(max_cost, item.cost);
        }
        return max_cost;
    }
};

#define REGISTER_SCALED_DP_SOLUTION(K)                \
using ScaledDPSolution_ ## K  = ScaledDPSolution<K>;  \
REGISTER_SOLUTION(ScaledDPSolution_ ## K);            \


template <class In>
Input ReadInput(In&& in) {
    Input input;
    in >> input.n >> input.W;
    for (int i = 0; i < input.n; ++i) {
        int cost;
        int weight;
        in >> cost >> weight;
        input.items.emplace_back(cost, weight, i + 1);
    }
    return input;
}

template <class Out>
void WriteOutput(Out&& out, const Output& output) {
    out << output.P << std::endl;
    for (const auto& item : output.items) {
        out << item.id << " ";
    }
}

bool ValidateOutput(const Input& input, const Output& output) {
    const auto sum_W = std::accumulate(output.items.begin(), output.items.end(), 0, [](int init, const auto& item) {
        return init + item.weight;
    });
    const auto sum_P = std::accumulate(output.items.begin(), output.items.end(), 0, [](int init, const auto& item) {
        return init + item.cost;
    });
    if (sum_W > input.W) {
        LOG("output weight is more than input.W");
        return false;
    }
    if (output.P != sum_P) {
        LOG("output.P is not equal to sum of items costs");
        return false;
    }
    std::unordered_set<int> ids;
    for (const auto& item : output.items) {
        ids.insert(item.id);
    }
    if (ids.size() != output.items.size()) {
        LOG("output.items has " << output.items.size() - ids.size() << " duplicates");
        return false;
    }
    return true;
}

void RunJudge() {
    const auto input = ReadInput(std::cin);
    Output best;
    for (const auto& [name, solution] : AllSolutions()) {
        const Output output = solution->Solve(input);
        if (best.P < output.P) {
            best = output;
        }
    }
    WriteOutput(std::cout, best);
}

void RunFileTest(const std::string& in_path, const std::string& out_path) {
    LOG("run test for " << in_path);

    const auto input = ReadInput(std::ifstream{in_path});
    LOG("input: n=" << input.n << ", W=" << input.W);

    std::string best_solution_name = "nope";

    Output best;
    for (const auto& [name, solution] : AllSolutions()) {
        LOG(name << ": start solution");

        const auto start_time = system_clock::now();

        const Output output = solution->Solve(input);

        const auto time_taken = duration_cast<milliseconds>(system_clock::now() - start_time).count();
        LOG(name << ": finish solution in " << time_taken << "ms");
        if (ValidateOutput(input, output)) {
            LOG(name << " output is valid, score is " << output.P);
            if (best.P < output.P) {
                LOG("got new best output with P=" << output.P << " from solution " << name);
                best = output;
                best_solution_name = name;
            }
        } else {
            LOG(name << " output is invalid, skip it");
        }

    }

    LOG("best score is " << best.P << ", best solution is " << best_solution_name);
    assert(ValidateOutput(input, best));

    LOG("output will be written to " << out_path << "." << best.P);
    WriteOutput(std::ofstream{out_path + "." + std::to_string(best.P)}, best);
}

int main(int argc, char** argv) {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(0);
    std::cout.tie(0);
    std::cerr.tie(0);

    if (argc == 1) {
        RunJudge();
    } else {
        RunFileTest(argv[1], argv[2]);
    }
}
